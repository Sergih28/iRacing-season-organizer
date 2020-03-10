# iRacing-season-organizer

This Python script gets the official iRacing PDF season schedule, and it creates an excel file in which we can customize our content and organize our season based on that, with multiple features (some of them not done yet).
For easier showing, I've shared the excel file [here](https://drive.google.com/file/d/1nIJnGKBl-SLz0TQ45uWtCKW1AB4_8X9k/view?usp=sharing) so you can copy it and see what it does at the moment. Beware that It'll change mostly everyday whenever I'm adding more functionalities (and hopefully not breaking current ones).

## Do you want to help?

We are open to ideas, either in the [iRacing's forum post](https://members.iracing.com/jforum/posts/list/3701367.page), creating an issue, or contacting me via [twitter](https://twitter.com/sergiheras).

I'm also considering creating a discord server (or a slack group) or incorporating a space for this into my own discord server.

## What I learned

- Python _venv_ (need to sort out a way so you can clone the repository and test it by yourself)
- Basic Python debugging with _pdb_
- PDF reading with Python's library Py2PDF
- XLS creation with Python's library _xlsxwritter_
- Python dictionaries usage

## Planning

1. Read PDF as 1st parameter
1. Save important data of every page in a big list or array
1. Write data in an XLS file
1. Improve with cool stuff the XLS file
