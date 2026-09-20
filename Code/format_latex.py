import re

with open('main.tex', 'r') as f:
    content = f.read()

# Replace documentclass and packages
new_preamble = r'''\documentclass[pdflatex,sn-basic]{sn-jnl}

\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{float}
\usepackage{subcaption}
\usepackage{xurl}

\begin{document}

\title[Accuracy Without Profit]{Accuracy Without Profit: A Statistical Evaluation of Machine Learning Profitability in the English Premier League}

\author*[1]{\fnm{Mostafa} \sur{Shams}}\email{mustafa.samy2022385@ci.menofia.edu.eg}
\affil*[1]{\orgdiv{Faculty of Computer and Information}, \orgname{Menoufia University}, \country{Egypt}}

\abstract{'''

abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
abstract_content = abstract_match.group(1).strip()

new_preamble += abstract_content + r'''}

\keywords{Machine Learning, Sports Economics, Probability Calibration, Kelly Criterion, Adaptive Markets Hypothesis, Concept Drift}

\maketitle
'''

intro_start = content.find(r'\section{Introduction}')
body_content = content[intro_start:]

# Add Declarations right before the bibliography
declarations = r'''
\section*{Declarations}
\begin{itemize}
    \item \textbf{Funding:} The author did not receive support from any organization for the submitted work. No funding was received to assist with the preparation of this manuscript.
    \item \textbf{Competing Interests:} The author has no relevant financial or non-financial interests to disclose.
    \item \textbf{Author Contributions:} Mostafa Shams is the sole author of this work. He conceived the study, conducted the data analysis, programmed the machine learning models, and wrote the entirety of the manuscript.
    \item \textbf{Data Availability:} All data, code, and statistical reports generated during this study are publicly available for review and replication at: \url{https://github.com/MostafaShams5/Predicting-EPL-Winners-But-Losing-Money-With-Data-Science}. The primary historical odds dataset is derived from Louis Chen's Kaggle repository (2021).
    \item \textbf{Ethical Approval:} Not applicable. This study relies exclusively on publicly available, anonymized sports data and involves no human or animal participants.
    \item \textbf{AI Assistant Disclosure:} An AI assistant (Antigravity) was used strictly for "AI assisted copy editing" purposes, providing formatting adjustments, grammatical refinement, and structural advice on the LaTeX manuscript. All generative analysis, theoretical framework, and code implementation are the original work of the author, who takes full accountability for the final text.
\end{itemize}

'''

body_content = body_content.replace(r'% --- BIBLIOGRAPHY ---', declarations + r'% --- BIBLIOGRAPHY ---')

with open('main.tex', 'w') as f:
    f.write(new_preamble + body_content)
