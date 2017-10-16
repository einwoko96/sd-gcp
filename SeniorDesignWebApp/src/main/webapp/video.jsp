<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">

    <title>Activity Recognition Dashboard</title>

    <!-- Bootstrap core CSS -->
    <link href="bootstrap.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="dashboard.css" rel="stylesheet">
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Activity Recognition Dashboard</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
            <li><a href="/index.jsp">Dashboard</a></li>
            <li><a href="/video.jsp">Video</a></li>
            <li><a href="#">Help</a></li>
          </ul>
          <form class="navbar-form navbar-right">
            <input type="text" class="form-control" placeholder="Search...">
          </form>
        </div>
      </div>
    </nav>

	<div id="container">
	    <form id="form" method="post" action="/infer" enctype="multipart/form-data">
	        <input type="file" name="pic" id="pic" accept="image/jpeg" />
	        <input type="submit" value="Submit" />
	    </form>
	</div>
    <div class="carousel-caption">
      <p><a class="btn btn-lg btn-primary" href="https://www.sanders.senate.gov/" role="button">Bernie would've won.</a></p>
      <br></br>
    </div>
	
    <div><input class="btn btn-info btn-space" type="submit" value="Submit" />
    <a href="/ofywebblog.jsp" class="btn btn-info btn-space" type="submit">Cancel</a></div>

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
            <li class="active"><a href="#">Overview <span class="sr-only">(current)</span></a></li>
            <li><a href="#">Reports</a></li>
            <li><a href="#">Analytics</a></li>
            <li><a href="#">Export</a></li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><a href="">Nav item</a></li>
            <li><a href="">Nav item again</a></li>
            <li><a href="">One more nav</a></li>
            <li><a href="">Another nav item</a></li>
            <li><a href="">More navigation</a></li>
          </ul>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h1 class="page-header">Display</h1>
          
	      <div class="container">
			  <div class="row">
				  <div class="col-sm-7 col-sm-offset-1">
					  <h2>16:9 Responsive Aspect Ratio</h2>
					  <div class="embed-responsive embed-responsive-16by9">
						  <iframe class="embed-responsive-item"
						    src="terrain_w1anmt8er__PM.mp4"></iframe>
					  </div>
				  </div>
			  </div>
		  </div>

          <h2 class="sub-header">Video Information</h2>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>UID</th>
                  <th>Label 1</th>
                  <th>Label 2</th>
                  <th>Label 3</th>
                  <th>Label 4</th>
                  <th>Label 5</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>Mountains</td>
                  <td>Sky</td>
                  <td>Flying</td>
                  <td>Driving</td>
                  <td>Falling</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="jquery.min.js"><\/script>')</script>
    <script src="bootstrap.js"></script>
  </body>
</html>
