# -*- coding: utf-8 -*-
import codecs
def pygooglevis_hs():
    name0 = codecs.open('tmp/enam.nme', 'r', 'utf-8')
    name = name0.read()
    fname = name.strip()
    name0.close()
    
    iput = file('input_hashtag.txt', 'r')
    iput_read = iput.readlines()
    output = codecs.open(fname + '_Hashtags.html', 'w', encoding='utf-8-sig')

    color0 = codecs.open('tmp/color.clr', 'r', 'utf-8')
    color = color0.read()
    color = eval(color.strip())
    color = color[1]
    color0.close

    print >> output, '<title>NodosApp: Top Hashtags</title>'
    print >> output, '<!-- jsHeader -->'
    print >> output, '<script type="text/javascript" src="http://www.google.com/jsapi">'
    print >> output, '</script>'
    print >> output, '<script type="text/javascript">'
    print >> output, ''
    print >> output, '// jsData'
    print >> output, 'function gvisDataBarChartIDc984298b9bf ()'
    print >> output, '{'
    print >> output, '    var data = new google.visualization.DataTable();'
    print >> output, '    var datajson ='
    print >> output, ' ['

    for i in iput_read:
        i = i.decode('utf-8-sig')
        i = i.encode('utf-8')
        i = i.split(' ')
        user = i[1].strip()
        count = i[0].strip()
        print >> output, '['
        print >> output, '"' + user + '",'
        print >> output, count
        print >> output, '],'
    print >> output, '];'    

    print >> output,'data.addColumn("string","hashtag");'
    print >> output,'data.addColumn("number","frecuencia");'
    print >> output,'data.addRows(datajson);'
    print >> output,'return(data);'
    print >> output,'}'
     
    print >> output,'// jsDrawChart'
    print >> output,'function drawChartBarChartIDc984298b9bf() {'
    print >> output,'  var data = gvisDataBarChartIDc984298b9bf();'
    print >> output,'  var options = {};'
    print >> output,'options["allowHtml"] = true;'
    print >> output,'options["width"] =    600;'
    print >> output,'options["series"] = [{color:"'+color+'"}];'
    print >> output,'options["hAxes"] = [{title:"Frecuencia"}];'
    print >> output,'options["vAxes"] = [{title:"Hashtag"}];'
    print >> output,'options["vAxis.title"] = "Usuario";'
    print >> output,'options["legend"] = "none";'
    print >> output,'options["backgroundColor"] = "transparent";'
    print >> output,'options["title"] = "Hashtags mas utilizados en Twitter";'

    print >> output,'     var chart = new google.visualization.BarChart('
    print >> output,'       document.getElementById("BarChartIDc984298b9bf")'
    print >> output,'     );'
    print >> output,'     chart.draw(data,options);'
    print >> output,'}'
     
    print >> output,'// jsDisplayChart '
    print >> output,'function displayChartBarChartIDc984298b9bf()'
    print >> output,'{'
    print >> output,'  google.load("visualization", "1", { packages:["corechart"] }); '
    print >> output,'  google.setOnLoadCallback(drawChartBarChartIDc984298b9bf);'
    print >> output,'}'
    print >> output,' '
    print >> output,'// jsChart '
    print >> output,'displayChartBarChartIDc984298b9bf()'
    print >> output,' '
    print >> output,'<!-- jsFooter -->  '
    print >> output,'//-->'
    print >> output,'</script>'
    print >> output,' '
    print >> output,'<!-- divChart -->'
    print >> output,'  '
    print >> output,'<div id="BarChartIDc984298b9bf"'
    print >> output,'  style="width: 600px; height: 500px;">'
    print >> output,'</div>'

    iput.close()
    output.close()

def pygooglevis_usr():
    name0 = codecs.open('tmp/enam.nme', 'r', 'utf-8')
    name = name0.read()
    fname = name.strip()
    name0.close()

    iput = codecs.open('input_usuarios.txt', 'r', 'utf-8')
    iput_read = iput.readlines()
    output = codecs.open(fname + '_Usuarios.html', 'w', 'utf-8')

    color0 = codecs.open('tmp/color.clr', 'r', 'utf-8')
    color = color0.read()
    color = eval(color.strip())
    color = color[1]
    color0.close
    
    print >> output, '<title>NodosApp: Top Mentions</title>'
    print >> output, '<!-- jsHeader -->'
    print >> output, '<script type="text/javascript" src="http://www.google.com/jsapi">'
    print >> output, '</script>'
    print >> output, '<script type="text/javascript">'
    print >> output, ''
    print >> output, '// jsData'
    print >> output, 'function gvisDataBarChartIDc984298b9bf ()'
    print >> output, '{'
    print >> output, '    var data = new google.visualization.DataTable();'
    print >> output, '    var datajson ='
    print >> output, ' ['

    for i in iput_read:
        i = i.split(' ')
        user = i[1].strip()
        count = i[0].strip()
        print >> output, '['
        print >> output, '"' + user.title() + '",'
        print >> output, count
        print >> output, '],'
    print >> output, '];'

    print >> output,'data.addColumn("string","hashtag");'
    print >> output,'data.addColumn("number","frecuencia");'
    print >> output,'data.addRows(datajson);'
    print >> output,'return(data);'
    print >> output,'}'
     
    print >> output,'// jsDrawChart'
    print >> output,'function drawChartBarChartIDc984298b9bf() {'
    print >> output,'  var data = gvisDataBarChartIDc984298b9bf();'
    print >> output,'  var options = {};'
    print >> output,'options["allowHtml"] = true;'
    print >> output,'options["width"] =    600;'
    print >> output,'options["series"] = [{color:"'+color+'"}];'
    print >> output,'options["hAxes"] = [{title:"Frecuencia"}];'
    print >> output,'options["vAxes"] = [{title:"Usuario"}];'
    print >> output,'options["vAxis.title"] = "Usuario";'
    print >> output,'options["legend"] = "none";'
    print >> output,'options["backgroundColor"] = "transparent";'
    print >> output,'options["title"] = "Usuarios mas mencionados en Twitter";'

    print >> output,'     var chart = new google.visualization.BarChart('
    print >> output,'       document.getElementById("BarChartIDc984298b9bf")'
    print >> output,'     );'
    print >> output,'     chart.draw(data,options);'
    print >> output,'}'
     
    print >> output,'// jsDisplayChart '
    print >> output,'function displayChartBarChartIDc984298b9bf()'
    print >> output,'{'
    print >> output,'  google.load("visualization", "1", { packages:["corechart"] }); '
    print >> output,'  google.setOnLoadCallback(drawChartBarChartIDc984298b9bf);'
    print >> output,'}'
    print >> output,' '
    print >> output,'// jsChart '
    print >> output,'displayChartBarChartIDc984298b9bf()'
    print >> output,' '
    print >> output,'<!-- jsFooter -->  '
    print >> output,'//-->'
    print >> output,'</script>'
    print >> output,' '
    print >> output,'<!-- divChart -->'
    print >> output,'  '
    print >> output,'<div id="BarChartIDc984298b9bf"'
    print >> output,'  style="width: 600px; height: 500px;">'
    print >> output,'</div>'

    iput.close()
    output.close()

def pygooglevis_twe():
    name0 = codecs.open('tmp/enam.nme', 'r', 'utf-8')
    name = name0.read()
    fname = name.strip()
    name0.close()
    
    iput = codecs.open('input_tweeters.txt', 'r', 'utf-8')
    iput_read = iput.readlines()
    output = codecs.open(fname + '_Tweeters.html', 'w', 'utf-8')

    color0 = codecs.open('tmp/color.clr', 'r', 'utf-8')
    color = color0.read()
    color = eval(color.strip())
    color = color[1]
    color0.close

    print >> output, '<title>NodosApp: Top Tweeters</title>'
    print >> output, '<!-- jsHeader -->'
    print >> output, '<script type="text/javascript" src="http://www.google.com/jsapi">'
    print >> output, '</script>'
    print >> output, '<script type="text/javascript">'
    print >> output, ''
    print >> output, '// jsData'
    print >> output, 'function gvisDataBarChartIDc984298b9bf ()'
    print >> output, '{'
    print >> output, '    var data = new google.visualization.DataTable();'
    print >> output, '    var datajson ='
    print >> output, ' ['

    for i in iput_read:
        i = i.split(' ')
        user = i[1].strip()
        count = i[0].strip()
        print >> output, '['
        print >> output, '"' + user.title() + '",'
        print >> output, count
        print >> output, '],'
    print >> output, '];'

    print >> output,'data.addColumn("string","hashtag");'
    print >> output,'data.addColumn("number","frecuencia");'
    print >> output,'data.addRows(datajson);'
    print >> output,'return(data);'
    print >> output,'}'
     
    print >> output,'// jsDrawChart'
    print >> output,'function drawChartBarChartIDc984298b9bf() {'
    print >> output,'  var data = gvisDataBarChartIDc984298b9bf();'
    print >> output,'  var options = {};'
    print >> output,'options["allowHtml"] = true;'
    print >> output,'options["width"] =    600;'
    print >> output,'options["series"] = [{color:"'+color+'"}];'
    print >> output,'options["hAxes"] = [{title:"Frecuencia"}];'
    print >> output,'options["vAxes"] = [{title:"Usuario"}];'
    print >> output,'options["vAxis.title"] = "Usuario";'
    print >> output,'options["legend"] = "none";'
    print >> output,'options["backgroundColor"] = "transparent";'
    print >> output,'options["title"] = "Usuarios con mas tweets en el tema";'

    print >> output,'     var chart = new google.visualization.BarChart('
    print >> output,'       document.getElementById("BarChartIDc984298b9bf")'
    print >> output,'     );'
    print >> output,'     chart.draw(data,options);'
    print >> output,'}'
     
    print >> output,'// jsDisplayChart '
    print >> output,'function displayChartBarChartIDc984298b9bf()'
    print >> output,'{'
    print >> output,'  google.load("visualization", "1", { packages:["corechart"] }); '
    print >> output,'  google.setOnLoadCallback(drawChartBarChartIDc984298b9bf);'
    print >> output,'}'
    print >> output,' '
    print >> output,'// jsChart '
    print >> output,'displayChartBarChartIDc984298b9bf()'
    print >> output,' '
    print >> output,'<!-- jsFooter -->  '
    print >> output,'//-->'
    print >> output,'</script>'
    print >> output,' '
    print >> output,'<!-- divChart -->'
    print >> output,'  '
    print >> output,'<div id="BarChartIDc984298b9bf"'
    print >> output,'  style="width: 600px; height: 500px;">'
    print >> output,'</div>'

    iput.close()
    output.close()
