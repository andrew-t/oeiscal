oeiscal
=======

People seem interested by unusual-looking dates. This meme, for example, gained a surprising amount of traction considering how strangely confused it is about how two-digit years correspond to four-digit ones:

> At exactly 06 mins and 07 seconds after 5 o’clock on Aug 9th 2010, it will be 05:06:07 08/09/10. This won’t happen again until the year 3010.
And then there's this one, which is just mad.

> AN INTERESTING FACT ABOUT AUGUST 2010. This August has 5 Sundays, 5 Mondays, 5 Tuesdays, all in one month. It happens once in 823 years.

All Augusts do that. Not always with Sunday, Monday and Tuesday, but near enough, and the exact combination isn't rare. Even if it were, the calendar loops every 400 years so nothing like this could possibly happen every 823. It would be an astonishing coincidence if the 1-in-823 freak August contained the 1-in-1000 freak county date thing.

But how impressive is the county date thing really? I mean, yes, it won't happen again until 2110, but if you use the UK date format it happened again in September. If you use the US date format, but write the time after the date, then it happened again later that morning.

And you don't have to start at five. You could start at six, and it happened in 2011. If you start at eight, and it will happen this December.

And you don't have to count in ones. You could do just the odd numbers. Or just the primes. Or...

So I did what anyone would do: I fired up Python, scraped the <a href="http://oeis.org/">Online Encyclopedia of Integer Sequences</a>, and <a href="http://twitter.com/823years">set my Raspberry Pi tweeting every interesting date it could find</a>

##Note

This is the Node.js version. Before starting, you need to run

    npm install twitter
    npm install q

