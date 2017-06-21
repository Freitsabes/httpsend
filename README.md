# httpsend
Super Simple Python Based HTTP(S) Send Tool For Api Testing

# Motivation
- The creator of this project acknowledges that tools like "Advanced REST Client", "Postman", "Paw" exist and that those tools are useful in certain scenarios.
- The creator of this project does not find those tools useful for an expert, for the following reasons:
  * They distribute a lot of information on different screens.
  * Their complexity brings bugs.
  * It is non-trivial to use them in a chain of other tools.
  * They are not fast.
  * They use proprietary data formats to store a collection of requests. Export to other formats do generally lack feature completeness and brings additional bugs.
- The creator of this project acknowledges that tools like curl exist to send requests with a single command line.
- The creator of this project finds curl incredibly useful for an expert but a bit too inconvenient.

# What is this thing doing?
- You write RFC 2068 / RFC 2616 / RFC 7230 compliant requests in files.
- You send them with this python skript.
- That is all.

# How-To:
python HTTPSend.py [-s] [-q] filename.http [filename1.http] ...

Skript works on files containing http requests in given order.  
If -s option is provided, use https  
If -q option is provided, do not print response  

freitsabes@gmail.com  
Possible future improvements:
- When folder is provided instead of files, go through files in folder alphabetically.
- add error handling
