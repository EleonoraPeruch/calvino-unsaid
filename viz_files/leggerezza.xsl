<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="xs"
  version="2.0">

  <xsl:output method="html"/>
  <xsl:template match="tei:TEI">
    <html>
      <head>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"/>
        <link rel="stylesheet" type="text/css" href="style.css"></link>
        <meta charset="UTF-8"/>
        <title>Lezioni americane</title>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        <script type="text/javascript" src="leggerezza.js"></script>
      </head>
      <body>
        <div class="container">
          <div class="row">
            <div class="col-sm-" style="margin-top: 3em">
              <div id="commands">
                <div style="margin-bottom: 3em">
                  <input type="radio" name="select" value="highlight" checked="checked"/> Highlight<br/>
                  <input id="searchText" type="text" value="" placeholder="search text to highlight"/>
                  <button id="highlight">Highlight</button>
                  <button id="reset" onclick="window.location.reload();">Reset</button><br/>
                </div>
                <div style="margin-bottom: 3em">
                  <button id="hist">Historical elements</button><br/>
                  <button id="cross">Cross-references</button><br/>
                  <button id="cogn">Cognitive level</button><br/>
                  <button id="interp">Interpretation</button><br/>
                  <button id="levels">Levels predominance</button><br/>
                </div>
                <div style="margin-bottom: 3em">
                  <ul>
                    <li id="hper">History:</li>
                    <li id="cper">Cross-referencing:</li>
                    <li id="gper">Cognition:</li>
                    <li id="iper">Interpretation:</li>
                    <li id="oper">None of the above:</li>
                  </ul>
                </div>
              </div>
             </div>
            <div id="content" class="col-sm" style="margin-left: 5em; margin-top: 3em">
              <xsl:apply-templates select="//tei:body/tei:head"/>
              <xsl:apply-templates select="//tei:div/tei:p"/>
              Cross-referenced people: <xsl:copy-of select="$people-cf"/><br/>
              Historical people: <xsl:copy-of select="$people-h"/>
            </div>
          </div>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="//tei:teiHeader"/>

  <xsl:template match="//tei:seg[@ana='#hist']">
    <seg ana="#hist">
      <xsl:apply-templates/>
    </seg>
  </xsl:template>

  <xsl:template match="//tei:seg[@ana='#interp']">
    <seg ana="#interp">
      <xsl:apply-templates/>
    </seg>
  </xsl:template>

  <xsl:template match="//tei:seg[@ana='#cogn']">
    <seg ana="#cogn">
      <xsl:apply-templates/>
    </seg>
  </xsl:template>

  <xsl:template match="//tei:seg[@type='person' and @ana='#cross-ref']">
    <seg type="person" ana="#cross-ref">
      <xsl:apply-templates/>
    </seg>
  </xsl:template>

  <xsl:template match="//tei:seg[@type='place' and @ana='#hist']">
    <seg type="place" ana="#hist">
      <xsl:apply-templates/>
    </seg>
  </xsl:template>

  <xsl:template match="//tei:body/tei:head">
    <h2>
      <xsl:apply-templates/>
    </h2>
  </xsl:template>

  <xsl:template match="//tei:div/tei:p">
    <p>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="//tei:lb">
    <xsl:apply-templates/><br/>
  </xsl:template>

  <xsl:template match="//tei:cit/tei:quote">
    <p style="font-size: 0.7em;">
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="//tei:title[@ana='#cross-ref']">
    <seg ana="#cross-ref"><em><xsl:apply-templates/></em></seg>
  </xsl:template>

  <xsl:template match="//tei:date[@ana='#hist']">
    <seg ana="#hist"><xsl:apply-templates/></seg>
  </xsl:template>

  <xsl:template match="//tei:date[@ana='#cross-ref']">
    <seg ana="#cross-ref"><xsl:apply-templates/></seg>
  </xsl:template>

  <xsl:template match="//tei:foreign">
    <em><xsl:apply-templates/></em>
  </xsl:template>

  <xsl:template match="tei:quote">
    <xsl:choose>
      <xsl:when test="not(@xml:lang='it') and not(@xml:lang='ver-it')">
        <em>
          <xsl:apply-templates/>
        </em>
      </xsl:when>
      <xsl:otherwise>
          <xsl:apply-templates/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:variable name="people-cf" select="count(//tei:seg[@type='person' and @ana='#cross-ref'])"/>
  <xsl:variable name="people-h" select="count(//tei:seg[@type='person' and @ana='#hist'])"/>

</xsl:stylesheet>
