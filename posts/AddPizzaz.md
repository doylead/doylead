---
title: Adding Pizzaz
date: 2024-10-21
---

# Adding Style to Substance

In the last [blog post](/posts/HelloWorld) I used Gemini Advanced to build a basic framework for a blog using NextJS as its front-end.

After that post I had seen Markdown elements translated into HTML markers, but those markers were not formatted in a way that made the blog posts look and feel like rendered markdown.

My goal this week was not to add new functionality per se, but to make reading posts from that blog more pleasurable using style elements (likely eventually rendered into CSS).

# "Conversations" with AI

The full transcripts with Gemini Advanced referenced in this post can be found [here](/transcripts/21-Oct-2024_AI).  I will use the titles Gemini generated for those conversations here as headers.

## NextJS Page Layout with Tailwind

Turns 1-3 were spent generating a React element I (eventually) asked to call Frame.  The idea is that this would serve as a default way of color blocking and adding navigation to the blog.  The fact this took three turns likely has more to do with the questions I asked and details I provided at each turn than anything else.

Turn 4 is a minor correction to the previous code to account for Typescript's strong typing.  Ideally this would not have required an additional turn, but Gemini did understand and correct the issue quickly.

In Turn 5 I asked for code to place spacing between paragraphs in rendered markdown.  Gemini provided me with code that just doesn't work for server-side components, and Turn 6 suggested I make the root layout a client-side component.  This seems a bit silly to me (but what do I know?) as we do not (yet) have any reason to require client-side behavior and I think it may come with a performance hit.

In Turn 7 I told Gemini I was not okay with using client-side components, and it agreed and it instead suggested using a static .CSS file.  I'm much happier with this suggestion.

In turn 8 Gemini put the behavior of finding and linking to bog posts in the new Frame component.  A relatively simple ask, and a job well done.

## Next.js Markdown Processing

Turn 1 was simply me providing my current code to prime the context window.  However, Gemini made several helpful suggestions I had not yet asked for (and may not have asked for).  I found this quite helpful in this case.

Turns 2 and 3 were me asking for code to make rendering markdown into a utility function (as it is used both by `app/posts/[slug]` and `app/transcripts[slug]`).  This once again likely took longer than it should have, as I did not specify that Gemini should use Typescript.

Turn 4 was a "correction" because Gemini had provided code for NextJS 13 (or earlier) when I was using NextJS 14.  Again, I could have been more specific with my question, and again Gemini was quick to find and correct the issue.

In Turn 5 I asked Gemini to re-introduce the suggestions it had initially made in Turn 1, including protection from cross-site scripting.

In Turns 6-15 I was troubleshooting the code provided in Turn 5.  In short, Gemini suggested syntax for the `rehype-attr` plugin which did not work, and for which I could not find any supporting evidence.  I provided Gemini with errors I was seeing in my IDE, I asked it for examples and documentation, and I generally got nowhere.  I believe this was hallucination, made worse by Gemini providing citations that may have created a sense of legitimacy (but were ultimately not relevant).

In Turn 16 I provided it with code that appeared to work (but used a different plugin).  To be fair, I'm not sure what I would have expected Gemini to respond with - I didn't ask a question.  Gemini just explained my code and its virtues to me.

In Turn 17 I had a more complete example and specifically asked Gemini for feedback.  It provided code that was significantly easier to read and extend, and provided a slight optimization to boot.

Once again, Turn 18 is asking Gemini to add the strong typing provided by Typescript.

## Filter then map for .md

In Turn 1 I asked Gemini to rewrite the part of the Frame component that lists blog posts for navigation.  I specifically asked Gemini to filter out any files that did not include the *.md extension, and it did so easiliy.

In Turn 2 I asked Gemini to provide sorting for those posts based on their metadata (so that newer posts would appear above older ones).  Once again, Gemini performed admirably.

## TL;DR

The biggest learning for me was to be more specific with the AI model.  For example, simply specificing that output should have been in Typescript would have saved several turns (and the time it took me to find those issues).

That said, I continue to be a bit disappointed in Gemini's ability to recover from some mistakes, at least in the same chat context window.  For all I know that syntax for `rehype-attr` was completely made up by Gemini, but it's hard even now for me to confidently say so.  Suffice it to say it's still necessary to approach these models skeptically.
