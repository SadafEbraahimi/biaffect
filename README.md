<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://stackedit.io/style.css" />
</head>

<body class="stackedit">
  <div class="stackedit__html"><h1 id="biaffect-sesor-fuser">Biaffect Sesor Fuser</h1>
<p><a href="http://forthebadge.com"><img src="http://forthebadge.com/images/badges/made-with-python.svg" alt="forthebadge"></a> <a href="http://forthebadge.com"><img src="http://forthebadge.com/images/badges/built-with-love.svg" alt="forthebadge"></a></p>
<p><img src="https://img.shields.io/badge/python-v3.6+-blue.svg" alt="Python"> <img src="https://img.shields.io/badge/code%20style-standard-green.svg" alt="Contributions welcome"> <img src="https://img.shields.io/badge/contributions-welcome-blue.svg" alt="Contributions welcome"></p>
<p>Sensor fusion is combining of sensory data or data derived from disparate sources such that the resulting information has less uncertainty than would be possible when these sources were used individually. Here we explain the application architecture and implementation of BiAffect’s Sensor Fuser. Project files are available on <a href="http://box.com">box.com</a>.</p>
<h2 id="table-of-contents">Table of Contents</h2>
<ul>
<li>
<p><a href="#how-it-works">How It Works</a></p>
</li>
<li>
<p><a href="#uml-diagram">UML diagram</a></p>
</li>
<li>
<p><a href="#classes">Classes</a></p>
<ul>
<li><a href="#user">User</a>
<ul>
<li><a href="#def-init">def __ init __()</a></li>
</ul>
</li>
</ul>
</li>
<li>
<p><a href="#acceleration">Acceleration</a><br>
- <a href="#init">def __ init __()</a><br>
- <a href="#def-motion">def motion()</a></p>
</li>
<li>
<p><a href="#gonogo">Gonogo</a><br>
- <a href="#init">def __ init __()</a><br>
- <a href="#def-error_rate">def error_rate()</a></p>
</li>
<li>
<p><a href="#keystroke">Keystroke</a><br>
- <a href="#init">def __ init __()</a><br>
- <a href="#def-keystroke_rate">def keystroke_rate()</a><br>
- <a href="#def-avg_interkey_delay">def avg_interkey_delay()</a></p>
</li>
<li>
<p><a href="#trailmaking">Trailmaking</a><br>
- <a href="#init">def __ init __()</a><br>
- <a href="#def-error_rate">def error_rate()</a></p>
</li>
<li>
<p><a href="#phq9">PHQ9</a><br>
- <a href="#init">def __ init __()</a><br>
- <a href="#def-calculating_phq9">def calculating_phq9()</a><br>
- <a href="#def-phq9_scoring">def phq9_scoring()</a><br>
- <a href="#def-most_recent_score">def most_recent_score()</a></p>
</li>
<li>
<p><a href="#mdq">MDQ</a><br>
- <a href="#init">def __ init __()</a><br>
- <a href="#def-calculating_mdq">def calculating_mdq()</a><br>
- <a href="#def-mdq_scoring">def mdq_scoring()</a><br>
- <a href="#def-most_recent_score">def most_recent_score()</a></p>
</li>
<li>
<p><a href="#reformat">Reformat</a><br>
- <a href="#def-apply_dir_change">def apply_dir_change()</a><br>
- <a href="#def-rename">def rename()</a></p>
</li>
<li>
<p><a href="#mdq">Main</a><br>
- <a href="#def-all_phq9">def all_phq9()</a><br>
- <a href="#def-all_mdq">def all_mdq()</a><br>
- <a href="#def-load_data">def load_data()</a><br>
- <a href="#def-extract_time">def extract_time()</a><br>
- <a href="#def-fuse">def fuse()</a></p>
</li>
<li>
<p><a href="#usage">Usage</a></p>
</li>
<li>
<p><a href="#authors">Authors</a></p>
</li>
</ul>
<h2 id="how-it-works">How It Works</h2>
<p>Here is a brief explanation of the software’s architecture and implementation:</p>
<ol>
<li>Renames all files in database with its owner’s health code.</li>
<li>Creates a class object <code>User</code>. Each user has some acceleration, keystroke, gonogo and trailmaking data. Also, each user has a PHQ9 and MDQ score. So class <code>User</code> has aggregation relationship with classes <code>Acceleration</code>, <code>Keystroke</code>, <code>Gonogo</code>, <code>Trailmaking</code>, <code>PHQ9</code> and <code>MDQ</code>.</li>
<li>Calculates all scores of each entry in PHQ9V1 and MDQv1 and saves them in lists.</li>
<li>Goes through each file in keystroke directory, loads all files of that user, extracts <code>%H:%M:%S</code> from <code>timestamp</code> column and adds it as a new column.<br>
… Here is where the magic happens!</li>
<li>Asks the user for the window size:<br>
24 hours: Detects the first and last use of user from keystroke file. Each user has <code>date of last use - date of first use</code> rows in output file.<br>
6 hours: Detects the first and last use of user from keystroke file. Each user has <code>(date of last use - date of first use) x 4</code> rows in output file. <code>00:00 AM - 05:59 AM, 06:00 AM - 11:59 AM, 12:00 PM - 05:59 PM, 06:00 PM - 11:59 PM</code><br>
4 rows: Detects the first and last use of user from keystroke file. Each user has 4 rows in output file. <code>00:00 AM - 05:59 AM, 06:00 AM - 11:59 AM, 12:00 PM - 05:59 PM, 06:00 PM - 11:59 PM</code></li>
<li>Breaks data down by locating all the rows that fall between the start and end of each window, stores them in a variable and sends the variable to fuser methods to receive results for that specific window.</li>
</ol>
<h2 id="uml-diagram">UML diagram</h2>
<p>Before going through the implementation, here is the class diagram of application:<br>
<img src="https://i.ibb.co/RSj0Gh0/Untitled-Diagram-1.png" alt="image"></p>
<h2 id="classes">Classes</h2>
<h3 id="user">User</h3>
<p>This class defines the behavior of each user. It has aggregation relationship with all other classes: each user has a health code, start and end of period, keystroke, acceleration, gonogo and trailmaking file, phq9 and mdq scores.<br>
We are probably going to change the architecture of this class in future updates.</p>
<h4 id="def-__-init-__">def __ init __()</h4>
<p>This method initializes each object of class User.</p>
<h3 id="acceleration">Acceleration</h3>
<h4 id="def-__-init-__-1">def __ init __()</h4>
<p>This method initializes each object of class Acceleration.</p>
<h4 id="def-motion">def motion()</h4>
<p>This method takes analysis_data of type numpy array as an argument, tracks the XYZ coordinates of a single point with Euclidean distance:<br>
<span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>m</mi><mi>o</mi><mi>t</mi><mi>i</mi><mi>o</mi><mi>n</mi><mo>=</mo><msqrt><mrow><msup><mi>x</mi><mn>2</mn></msup><mo>+</mo><msup><mi>y</mi><mn>2</mn></msup><mo>+</mo><msup><mi>z</mi><mn>2</mn></msup></mrow></msqrt></mrow><annotation encoding="application/x-tex">motion=\sqrt{x^2+y^2+z^2}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 0.65952em; vertical-align: 0em;"></span><span class="mord mathit">m</span><span class="mord mathit">o</span><span class="mord mathit">t</span><span class="mord mathit">i</span><span class="mord mathit">o</span><span class="mord mathit">n</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 1.24em; vertical-align: -0.233291em;"></span><span class="mord sqrt"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.00671em;"><span class="svg-align" style="top: -3.2em;"><span class="pstrut" style="height: 3.2em;"></span><span class="mord" style="padding-left: 1em;"><span class="mord"><span class="mord mathit">x</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.740108em;"><span class="" style="top: -2.989em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mord"><span class="mord mathit" style="margin-right: 0.03588em;">y</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.740108em;"><span class="" style="top: -2.989em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mord"><span class="mord mathit" style="margin-right: 0.04398em;">z</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height: 0.740108em;"><span class="" style="top: -2.989em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span></span></span></span><span class="" style="top: -2.96671em;"><span class="pstrut" style="height: 3.2em;"></span><span class="hide-tail" style="min-width: 1.02em; height: 1.28em;"><svg width="400em" height="1.28em" viewBox="0 0 400000 1296" preserveAspectRatio="xMinYMin slice"><path d="M263,681c0.7,0,18,39.7,52,119c34,79.3,68.167,
158.7,102.5,238c34.3,79.3,51.8,119.3,52.5,120c340,-704.7,510.7,-1060.3,512,-1067
c4.7,-7.3,11,-11,19,-11H40000v40H1012.3s-271.3,567,-271.3,567c-38.7,80.7,-84,
175,-136,283c-52,108,-89.167,185.3,-111.5,232c-22.3,46.7,-33.8,70.3,-34.5,71
c-4.7,4.7,-12.3,7,-23,7s-12,-1,-12,-1s-109,-253,-109,-253c-72.7,-168,-109.3,
-252,-110,-252c-10.7,8,-22,16.7,-34,26c-22,17.3,-33.3,26,-34,26s-26,-26,-26,-26
s76,-59,76,-59s76,-60,76,-60z M1001 80H40000v40H1012z"></path></svg></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.233291em;"><span class=""></span></span></span></span></span></span></span></span></span></span><br>
It returns the length and average motion of all data received from <code>analysis_data</code>.<br>
Python floats are neither arbitrary precision, nor of unlimited size. Data stored in some acceleration files are too large to be stored in double precision float. The <code>decimal</code> library allows arbitrary precision and can handle the size. We used <code>decimal</code> to go beyond hardware limitations and solve overflow problem.</p>
<h3 id="gonogo">Gonogo</h3>
<h4 id="def-__-init-__-2">def __ init __()</h4>
<p>This method initializes each object of class Gonogo.</p>
<h4 id="def-error_rate">def error_rate()</h4>
<p>This method takes <code>analysis_data</code> of type numpy array as an argument, calculates rate of cells in <code>incorrect</code> column which are <code>True</code>.</p>
<h3 id="keystroke">Keystroke</h3>
<h4 id="def-__-init-__-3">def __ init __()</h4>
<p>This method initializes each object of class Keystroke.</p>
<h4 id="def-keystroke_rate">def keystroke_rate()</h4>
<p>This method takes analysis_data of type numpy array as an argument, calculates the rate of cells in <code>alphanum</code> column which are <code>backspace</code> and <code>autocorrection</code>.</p>
<h4 id="def-avg_interkey_delay">def avg_interkey_delay()</h4>
<p>This method takes analysis_data of type numpy array as an argument, calculates the average delay between each tap by using data in <code>keypress_timestamp</code> column.</p>
<h3 id="trailmaking">Trailmaking</h3>
<h4 id="def-__-init-__-4">def __ init __()</h4>
<p>This method initializes each object of class Trailmaking.</p>
<h4 id="def-error_rate-1">def error_rate()</h4>
<p>This method takes analysis_data of type numpy array as an argument, calculates rate of cells in <code>incorrect</code> column which are <code>False</code>.</p>
<h3 id="phq9">PHQ9</h3>
<h4 id="def-__-init-__-5">def __ init __()</h4>
<p>This method initializes each object of class PHQ9.</p>
<h4 id="def-calculating_phq9">def calculating_phq9()</h4>
<p>This is a static method of class PHQ9. It simply receives user’s answers to questionnaire and calculates PHQ9 score.</p>
<h4 id="def-phq9_scoring">def phq9_scoring()</h4>
<p>This is a static method of class PHQ9. When a user answers a question it records a score.</p>

<table>
<thead>
<tr>
<th align="left">Answer</th>
<th align="center">Score</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">Not at all</td>
<td align="center">0</td>
</tr>
<tr>
<td align="left">Not difficult at all</td>
<td align="center">1</td>
</tr>
<tr>
<td align="left">Several days</td>
<td align="center">2</td>
</tr>
<tr>
<td align="left">More than half the days</td>
<td align="center">3</td>
</tr>
<tr>
<td align="left">Nearly every day</td>
<td align="center">4</td>
</tr>
</tbody>
</table><h4 id="def-most_recent_score">def most_recent_score()</h4>
<h3 id="mdq">MDQ</h3>
<h4 id="def-__-init-__-6">def __ init __()</h4>
<p>This method initializes each object of class MDQ.</p>
<h4 id="def-calculating_mdq">def calculating_mdq()</h4>
<p>This is a static method of class MDQ. It simply receives user’s answers to questionnaire and calculates MDQ score.</p>
<h4 id="def-mdq_scoring">def mdq_scoring()</h4>
<p>This is a static method of class MDQ. It scores each user’s answer.</p>

<table>
<thead>
<tr>
<th align="left">Answer</th>
<th align="center">Score</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">True</td>
<td align="center">1</td>
</tr>
<tr>
<td align="left">False</td>
<td align="center">0</td>
</tr>
</tbody>
</table><h3 id="reformat">Reformat</h3>
<h4 id="def-apply_dir_change">def apply_dir_change()</h4>
<p><code>acc_dir</code>, <code>gonogo_dir</code>, <code>keystroke_dir</code> and <code>trailmaking_dir</code> are directories which you are supposed to copy all your data in them. Array <code>new_dir</code> holds new directories for data.  This method passes old directory and new directory to <code>rename()</code> method.</p>
<h4 id="def-rename">def rename()</h4>
<p>This method checks the type of file first. For example if receives a directory which contains gogono files, the prefix of the new name is <code>gonogo-</code>. Then it opens all files in the directory that it received as an argument, finds health codes of all users and saves the old name of file and health code in that file in <code>health_codes</code> list. Then it converts the list to <code>old_new</code> numpy array. So <code>old_new</code> looks something like this:</p>

<table>
<thead>
<tr>
<th align="left">old_new[0]</th>
<th align="center">old_new[1]</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">GoNoGoJSONs_77.csv</td>
<td align="center">72a15fb2-ab5d-4f7b-9485-c0b0e5754558</td>
</tr>
</tbody>
</table><p>In the final step, it iterates through <code>old_new</code> and renames all files into new directory. Here are some examples:</p>

<table>
<thead>
<tr>
<th align="left">Before (data/{filetype})</th>
<th align="center">After (renamed_data/{filetype}</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left">accelerationJSON_309</td>
<td align="center">acceleration-128a814f-16d4-4d01-b7d7-14e404a8d27b</td>
</tr>
<tr>
<td align="left">keystrokeJSONdiag_33</td>
<td align="center">keystroke-cb8cc840-1890-4d51-b28c-53dd588485f4</td>
</tr>
<tr>
<td align="left">GoNoGoJSONs_78</td>
<td align="center">gonogo-5c0de347-0572-4601-8464-a59d18371751</td>
</tr>
<tr>
<td align="left">trailMaking_8</td>
<td align="center">trailmaking-3ec343db-1a5c-4087-a86f-0b7623b7a80a</td>
</tr>
</tbody>
</table><h3 id="main">Main</h3>
<h4 id="def-all_phq9">def all_phq9()</h4>
<p>This method opens file <code>PHQ9V1.csv</code>, reads each line and sends it to <code>calculating_phq9</code> static method of class PHQ9, receives scores of each line and appends it to list <code>phq9_results</code>. List <code>phq9_results</code> have <code>healthCode</code>, <code>uploadeDate</code>, <code>ROW_ID</code> and <code>score</code> columns.</p>
<h4 id="def-all_mdq">def all_mdq()</h4>
<p>This method opens file <code>MDQv1.csv</code>, reads each line and sends it to <code>calculating_mdq</code> static method of class MDQ, receives a score of each line and appends it to list <code>mdq_results</code>. List <code>mdq_result</code>s have <code>healthCode</code>, <code>uploadeDate</code>, <code>ROW_ID</code>, <code>severity</code> and <code>bipolar</code> columns.</p>
<h4 id="def-load_data">def load_data()</h4>
<p>This method receives a keystroke file and the health code in it and looks for acceleration, gonogo and trailmaking file of that user, applies <code>timezone</code> to <code>timestamp</code> column, extracts %H:%M:%S from timestamp column and adds it as a new column named <code>time</code>.</p>
<h4 id="def-extract_time">def extract_time()</h4>
<p>This method takes <code>x</code> of type string as an argument, converts it to timestamp and extracts the time part of it.</p>
<h4 id="def-fuse">def fuse()</h4>
<p>This method is heart of the application. It creates instance variables of all classes, receives data frames of specific size, calculates the next frame and fills each window of an instance variable of class <code>User</code> with its data.</p>
<h2 id="usage">Usage</h2>
<p>Since files in database are randomly named and it is not obvious which file belongs to a specific user, we decided to rename all files with <code>type of file-healthcode.csv</code>.<br>
For example, <code>accelerationJSON_290.csv' changes to 'acc-d5c3c818-59fd-4368-8733-ef7b6ba985e6</code>.<br>
Before running the application, copy all the files into root/data/{folder}. Also copy PHQ9V1 and MDQv1 into <code>root/data</code>. Note that application makes changes to the original data, renames all files and moves them to directory <code>root/src/renamed/data</code>.<br>
You can export results into csv file with frames of 24 hours, 6 hours and average of 6 hours.<br>
Now all you need to do is:</p>
<pre><code>$ python main.py &lt;'24hours', '6hours', '4rows'&gt;  
</code></pre>
<p>As an example, if you want frames of 24 hour, this is the command:</p>
<pre><code>$ python main.py 24hours  
</code></pre>
<p>If there are still some files left in root/data/{folder}, it means those files are empty.</p>
<h2 id="authors">Authors</h2>
<ul>
<li><strong>Sadaf Ebrahimi</strong> - <a href="https://linkedin.com/in/sadafebraahimi">LinkedIn</a></li>
</ul>
</div>
</body>

</html>
