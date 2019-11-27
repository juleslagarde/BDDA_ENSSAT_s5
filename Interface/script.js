
async function hierarchy(){
  p1.style.display = ""
  p2.style.display = "none"


  format = d3.format(",d")
  width = 932
  radius = width / 6
  arc = d3.arc()
      .startAngle(d => d.x0)
      .endAngle(d => d.x1)
      .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
      .padRadius(radius * 1.5)
      .innerRadius(d => d.y0 * radius)
      .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1))
  partition = data => {
    const root = d3.hierarchy(data)
        .sum(d => d.value)
        .sort((a, b) => b.value - a.value);
    return d3.partition()
        .size([2 * Math.PI, root.height + 1])  (root);
  }
  data = await $.get("hierarchy?filename="+p1_fileName.value.replace(/ */g, "")+"&parts="+JSON.stringify(p1_parts.value.replace(/ */g, "").split(">"))  )
  // data = JSON.parse(data);
  color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, data.children.length + 1))
  const root = partition(data);

  root.each(d => d.current = d);

  d3.select("#svg1>svg").remove()
  const svg = d3.select("#svg1").append("svg")
      .attr("width", width)
      .attr("height", width)
      .style("font", "10px sans-serif");

  const g = svg.append("g")
      .attr("transform", `translate(${width / 2},${width / 2})`);

  const path = g.append("g")
      .selectAll("path")
      .data(root.descendants().slice(1))
      .join("path")
        .attr("fill", d => { while (d.depth > 1) d = d.parent; return color(d.data.name); })
        .attr("fill-opacity", d => arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0)
        .attr("d", d => arc(d.current));

  path.filter(d => d.children)
      .style("cursor", "pointer")
      .on("click", clicked);

  path.append("title")
      .text(d => `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${format(d.value)}`);

  const label = g.append("g")
      .attr("pointer-events", "none")
      .attr("text-anchor", "middle")
      .style("user-select", "none")
    .selectAll("text")
    .data(root.descendants().slice(1))
    .join("text")
      .attr("dy", "0.35em")
      .attr("fill-opacity", d => +labelVisible(d.current))
      .attr("transform", d => labelTransform(d.current))
      .text(d => d.data.name);

  const parent = g.append("circle")
      .datum(root)
      .attr("r", radius)
      .attr("fill", "none")
      .attr("pointer-events", "all")
      .on("click", clicked);

  function clicked(p) {
    parent.datum(p.parent || root);

    root.each(d => d.target = {
      x0: Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
      x1: Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
      y0: Math.max(0, d.y0 - p.depth),
      y1: Math.max(0, d.y1 - p.depth)
    });

    const t = g.transition().duration(750);

    // Transition the data on all arcs, even the ones that aren’t visible,
    // so that if this transition is interrupted, entering arcs will start
    // the next transition from the desired position.
    path.transition(t)
        .tween("data", d => {
          const i = d3.interpolate(d.current, d.target);
          return t => d.current = i(t);
        })
      .filter(function(d) {
        return +this.getAttribute("fill-opacity") || arcVisible(d.target);
      })
        .attr("fill-opacity", d => arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0)
        .attrTween("d", d => () => arc(d.current));

    label.filter(function(d) {
        return +this.getAttribute("fill-opacity") || labelVisible(d.target);
      }).transition(t)
        .attr("fill-opacity", d => +labelVisible(d.target))
        .attrTween("transform", d => () => labelTransform(d.current));
  }

  function arcVisible(d) {
    return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
  }

  function labelVisible(d) {
    return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
  }

  function labelTransform(d) {
    const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
    const y = (d.y0 + d.y1) / 2 * radius;
    return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
  }
}
async function associativity(){
  p1.style.display = "none"
  p2.style.display = ""

  margin = ({top: 20, right: 0, bottom: 120, left: 40})
  height = 300
  width = 900

  xAxis = g => g
      .attr("transform", `rotate(45)`)
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickSizeOuter(0))
      .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)")
  yAxis = g => g
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y))
      .call(g => g.select(".domain").remove())

  data = await $.get("associativity?filename="+p2_fileName.value.replace(/ */g, "")+"&filter="+JSON.stringify(p2_filter.value.replace(/ */g, "").split(":"))  )//.sort((a, b) => b.value - a.value)
  atypic = data["atypic"]
  data = data["assoc"].filter(d=>d.value>0)

  x = d3.scaleBand()
      .domain(data.map(d => d.name))
      .range([margin.left, width - margin.right])
      .padding(0.1)
  y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)]).nice()
      .range([height - margin.bottom, margin.top])

  d3.select("#svg2>svg").remove()
  const svg = d3.select("#svg2").append("svg")
      .attr("viewBox", [0, 0, width, height]);

  svg.append("g")
      .attr("fill", "steelblue")
      .selectAll("rect")
      .data(data)
      .join("rect")
      .attr("x", d => x(d.name))
      .attr("y", d => y(d.value))
      .attr("height", d => y(0) - y(d.value))
      .attr("width", x.bandwidth());


  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);

  alert("Le terme le plus atypique est '"+atypic["name"]+"' (coef d'atypicité : "+atypic["value"]+")")
}

let p1_fileName, p1_parts, p2_fileName, p2_filter, p1, p2;

window.onload = async function onload(){
  p1_fileName = $("#p1_fileName")[0]
  p1_parts = $("#p1_parts")[0]
  p2_fileName = $("#p2_fileName")[0]
  p2_filter = $("#p2_filter")[0]
  p1 = $("#page1")[0]
  p2 = $("#page2")[0]
  p1_fileName.onchange = hierarchy
  p1_parts.onchange = hierarchy
  p2_fileName.onchange = associativity
  p2_filter.onchange = associativity
  p1.style.display = "none"
  p2.style.display = "none"



  await hierarchy()
}
