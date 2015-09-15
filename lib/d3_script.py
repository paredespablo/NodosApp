import networkx as nx
import codecs
import operator

def d3():

    nombre3 = file('tmp/enamgexf.nme', 'r')
    nombre2 = nombre3.read()
    nombre = nombre2.strip()
    nombre3.close()

    output = codecs.open(str(nombre) + 'html', 'w', 'utf-8')

    templatea = '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>NodosApp D3 project</title>
    <style>

    .node {
      stroke: #fff;
      stroke-width: 1.5px;
    }

    .link {
      stroke: #999;
      stroke-opacity: .6;
    }

    hr { display: block; height: 1px;
        border: 0; border-top: 1px solid #ccc;
        margin: 1em 0; padding: 0; }

    </style>

    <script src="http://d3js.org/d3.v3.min.js"></script> 

    </head>

    <body>
      <div id='PopUp' 
    style='display: none; position: absolute; left: 10px; top: 50px; border: solid gray 1px; padding: 1px; background-color: whitesmoke; text-align: justify; font-size: 12px; color: black; width: 135px; opacity:0.6; filter:alpha(opacity=60); '>
    <center id='PopUpText'>TEXT</center>
    </div>

    <script>

    //var width = 960, height = 500;

    var width = 800,
        height = 600;


    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(-60)
        .linkDistance(30)
        .size([width, height]);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    var graph = {'''

    print >> output, templatea



    G = nx.read_gexf('tmp/tmpfile.gexf', relabel=False)

    PR = nx.pagerank(G, alpha=0.85)
    nodos = sorted(PR.iteritems(), key=operator.itemgetter(1), reverse=True)
    nodos_aux = []
    val_aux = []
    
    for k in nodos:
        nodos_aux.append(k[0])
        val_aux.append(k[1])

        
    edges = G.edges()
    print >> output, '"nodes":['
    for i in nodos_aux:
        pos = nodos_aux.index(i)
        if (pos < 200):
            name = i
            val = val_aux[pos]
            val2 = int(val*100)
            print >> output, '{'
            #print >> output, '  "relevance": 1,'
            print >> output, '  "relevance": '+str(val2)+','
            print >> output, '  "name": "'+ name + '",'
            print >> output, '  "root":"false",'
            print >> output, '  "url":"",'
            print >> output, '  "id":'+str(pos)+''
            
            total = len(nodos) -1
            if pos == total:
                print >> output, '}'
            else:
                print >> output, '},'
        else:
            pass

    print >> output, '],'
    print >> output, '"links":['
    print >> output,  ''

    for i in edges:
        emisor = i[0]
        receptor = i[1]
        emisor2 = nodos_aux.index(emisor)
        receptor2 = nodos_aux.index(receptor)
        if (emisor2 < 200) and (receptor2 < 200):
            print >> output, '{'
            print >> output, '  "source": '+str(emisor2)+','
            print >> output, '  "target": '+str(receptor2)+','
            print >> output, '  "value": 1'
            print >> output, '},'
        else:
            pass

    print >> output, ']'
    print >> output, '};'

    templateb = '''


      force
          .nodes(graph.nodes)
          .links(graph.links)
          .start();

      var link = svg.selectAll("line.link")
          .data(graph.links)
          .enter().append("line")
          //.attr("class", "link")
          .attr("class",  function(d) {
                return "link source-" + d.source.id + " target-" + d.target.id;
          })
          .style("stroke-width", function(d) { return Math.sqrt(d.value); });

      var node = svg.selectAll("circle.node")
          .data(graph.nodes)
          .enter().append("circle")
          .attr("class", "node")
          .attr("r", function(d)  //radio de los nodos
            { 
              return d.relevance + 5;
            })
          .style("fill", function(d) { return color(d.group); })
          
          .on("mouseover", function(d)
            {
              var el, x, y;

              document.getElementById('PopUpText').innerHTML = d.name;

              el = document.getElementById('PopUp')        
              el.style.left = d.x + "px";
              el.style.top = d.y + "px";        
              el.style.display = 'block';
              
              svg.selectAll("line.link.target-" + d.id).classed("target", true).style("stroke", 'black'); 
              svg.selectAll("line.link.source-" + d.id).classed("source", true).style("stroke", 'black');

              svg.selectAll("line.link.target-" + d.id).classed("target", true).style("stroke-width", function(d) { return 2*Math.sqrt(d.value); }); 
              svg.selectAll("line.link.source-" + d.id).classed("source", true).style("stroke-width", function(d) { return 2*Math.sqrt(d.value); });
            })


            .on("mouseout", function(d)
            {
              document.getElementById('PopUp').style.display = 'none';
              
              svg.selectAll("line.link.target-" + d.id).classed("target", false).style("stroke", "#CCC");;
              svg.selectAll("line.link.source-" + d.id).classed("source", false).style("stroke", "#CCC");

              svg.selectAll("line.link.target-" + d.id).classed("target", true).style("stroke-width", function(d) { return Math.sqrt(d.value); }); 
              svg.selectAll("line.link.source-" + d.id).classed("source", true).style("stroke-width", function(d) { return Math.sqrt(d.value); });
            })
          
          .call(force.drag);

      /* node.append("title")
          .text(function(d) { return d.name; }); */

      force.on("tick", function() {

        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
      });


    </script>
    </body>
    </html>
    '''

    print >> output, templateb

    output.close()
    print 'Grafico D3 finalizado'
