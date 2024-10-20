---
title: Hello, World
date: 2024-10-15
---

# Background Noise and Context

A few notable events immediately preceed this work:

- On August 26th, 2024 I got access to Gemini Advanced, Google's flagship consumer AI product (as a promotion, because I bought a Pixel 9 Pro XL).
- On September 12th, 2024 OpenAI released it's o1 model preview.
- On October 11th, 2024 a coworker I trust told me that they believed candidates for software engineering roles would be better served by experience using AI than experience developing software.

I have had a lot of fun asking it to rank whether various things are sandwiches (apparently burritos are sandwiches, tacos are not).  That said, I've been hesitant to use AI more seriously.  I think this has come down to two major arguments:
1) AI can "hallucinate," or produce nonsense results.  It's essentially a meme that AI models have told people to [eat rocks and glue](https://www.thedailybeast.com/google-explains-why-its-ai-overviews-told-users-to-eat-rocks-and-glue-pizzas)
1) There's a sense of stolen valor in AI.  I've completed 10 of 12 courses for a master's degree in Software Engineering, and it's humbling to think that the skills I worked so hard to develop may be trivialized by new technology

While these two arguments are both worth *something*, as time goes on I've lost confidence they can justify *not personally experiencing* AI in a development context.  I can conduct a series of experiments to figure out what AI is currently good at, what it's not currently good at, and how it could help me in my work.

This project is my attempt to study and use AI to develop software.

## Setting Up A Blog

The full transcript with Gemini Advanced referenced in this post can be found [here](/transcripts/15-Oct-2024_AI).

I've historically avoided front-end work.  Making "artistic" choices has always felt more stressful to me than working with APIs.  That said, just accepting a skills gap is not conducive to growth.  

I've been following along with a [tutorial on NextJS](https://nextjs.org/learn) for a while now, and I can imagine wanting to use this framework for future projects.

This is my first challenge for AI: to help me set up one of the simplest projects I could think of - the site that will eventually publish articles like this one.  In this case I worked with Gemini Advanced (which I'll routinely shorten to "Gemini") as I have access at no additional cost.

I'll use the word "turn" to refer to the pair of my prompt to Gemini and its response.

In Turn 1 Gemini impressed me by outlining several different approaches for setting up a blog, including (unprompted) providing a list of pros and cons for each.  One major hurdle to any project is picking a starting point, and I have to say I really prefer this type of well laid-out list to search results which often have motives that don't align with mine (e.g. selling their service).

In Turn 2 Gemini went on to specify code for multiple files to build a cohesive NextJS project.  It's cool that it clearly understands enough about NextJS to understand the logic of what files exist and where they're located, but it's important to note that the code provided both (1) contains fatal bugs and (2) does not (yet) render markdown from input files (instead showing plain text).  More on both later.

Gemini and I then spent considerable time and effort debugging an error in my local project configuration.  I provided Gemini with the information and error messages available to me, with which Gemini was able to correctly diagnose the problem (a version conflict because I was using NextJS 15).  Unfortunately, the steps Gemini provided did not *solve* the problem.  I ended up simply creating a new NextJS project.

In Turns 10 and 12 I provided error messages from running the code it provided earlier.  Gemini quickly diagnosed both errors and issued corrections.  Granted, the correction in Turn 10 came after a lot of text about how *I* could detect the problem.  This could be helpful in some contexts, but in this case I actually missed the corrected code snippet (so in Turn 11 I essentially asked that be regenerated).  While I have to dock Gemini some points for making these errors in the first place, I have to say it did a good job of addressing them.

In Turn 13 I told Gemini that the blog based on the provided code displayed the heading and text of a markdown post, but did not render markdown elements (headers, code blocks, et cetera).  Gemini was quick to understand why Markdown was not rendering, and to offer two possible paths forward.  However, compared to Turn 1 when asking for options on setting up a blog to begin with, Gemini did not immediately provide a list of pros and cons.  I asked it to do so in Turn 14, and it complied.

In Turn 15 it corrected what appeared to be a model formatting error with code using `react-markdown`, which worked quickly afterwards.  However, this did not offer the type of code syntax highlighting I was hoping for.

In Turn 16 I asked for and received a baseline for using `remark` and `rehype`.  However, this code simply did not work as written.  I repeatedly got 404 errors, which I spent considerable time (Turns 17-41) attempting to debug with Gemini, mostly unsuccessfully.  I think we discovered some unrelated errors as I pointed to various messages in network traces, my IDE, and the developer console, so I don't want to call this useless.  But it certainly wasn't "bam, here's markdown."

In Turn 42 I was tired of troubleshooting issues with (I believe) `rehypeRaw` and so I found a [blog post](https://ondrejsevcik.com/blog/building-perfect-markdown-processor-for-my-blog) written by another person which detailed their setup for rendering Markdown.  I provided this to Gemini and asked it to use their code as an example, which it did successfully.

**TL;DR** - Overall, I'm impressed with Gemini.  Among other things, it:
* Provided detailed suggestions on how to set up a project, notably including different approaches and the benefits and drawbacks to those differing approaches
* Understood NextJS project structure and several markdown-based libraries
* Provided starter code
* Accurately diagnosed issues based on error messages and other diagnostics


However, there was some room for improvement, namely:
* Starter code provided had several bugs/errors
* Starter code did not actually have all requested functionality
* Extended troubleshooting sessions were a **chore**.  Gemini was very helpful for a few prompts, but could get caught in circles after that.  I found myself turning to web searches as I lost confidence in Gemini for issues it could not solve fairly quickly
