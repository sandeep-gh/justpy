# JustPy


## Introduction
JustPy-Svelte is JustPy framework (https://github.com/justpy-org/justpy) with Svelte (https://svelte.dev/) being used  the underlying frontend engine  instead of Vue. 

JustPy-Svelte is not as feature complete as Justpy. Many frontend utitiles that were build on 
Vue engine are not supported here. Specifically,
- AGGRID
- AGGRID_ENTERPRISE
- BOKEH
- DECKGL
- HIGHCHARTS
- KATEX
- PLOTLY
- QUASAR
- QUASAR_VERSION
- VEGA



## Why Svelte
Code readability, especially for non-javascript programmers, was the primary reason for porting Justpy over to Svelte. Vue on its own is powerful, has be around for longer, and has large ecosystem of libraries/tools build around it. However, I felt it not an easy framework to pick up and comprehend, especially for non-javascript programmers. 

Comparatively, programming in  Svelte is much more straightforward and easy to comprehend 
for programmers coming from C/C++/Python/Java background. 

Its yet to be seen if Svelte offers any other advantages over Vue. 
There is good reason to hope for that. Svelte is a newer runtime and has 
very different architecture and execution paradigm, which could yield some 
advantages like being more responsive, executing faster, and better
coordination between Python runtime backend with the Javascript/Svelte frontend. 



## Docs and Tutorials
[JustPy Docs and Tutorials](https://justpy.io)

