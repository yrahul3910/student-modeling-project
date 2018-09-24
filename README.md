# Student Modeling Project
This is the final year project developed. It implements an Intelligent Tutoring System (ITS), using models from literature. The report, papers, and the code are open and uploaded here.

# Links to Papers
The following papers have been helpful in understanding current approaches to student modeling.
* [Spaulding et al., 2016. Affect-Aware Student Models for Robot Tutors](http://www.samspaulding.com/resources/Spaulding_AAMAS16.pdf)
* Corbett and Anderson, 1994. Knowledge Tracing: Modeling the acquisition of procedural knowledge. Unfortunately, this is not available for free.
* [Lin and Chi, 2017. Comparisons of BKT, RNN and LSTM for Predicting Student Learning Gains](https://people.engr.ncsu.edu/mchi/pdfs/AIED2017_LianaFinal.pdf)
* [Lin et al., 2016. Incorporating Student Response Time and Tutor Instructional Interventions into Student Modeling](https://people.engr.ncsu.edu/mchi/pdfs/Umap_Liana2016_v2.pdf)
* [Lin and Chi, 2016. Intervention-BKT: Incorporating Instructional Interventions into Bayesian Knowledge Tracing](https://people.engr.ncsu.edu/mchi/pdfs/ITS_2016_Liana.pdf)
* [David et al., 2016. Sequencing Educational Content in Classrooms using Bayesian Knowledge Tracing](http://www.ise.bgu.ac.il/faculty/kobi/Papers/bkt.pdf)
* [Schultz and Arroyo, 2015. Tracing Knowledge and Engagement in Parallel in an Intelligent Tutoring System](https://www.researchgate.net/publication/280156170_Tracing_Knowledge_and_Affect_in_Parallel_in_an_Intelligent_Tutoring_System)
* [Piech et al., 2015. Deep knowledge tracing](https://web.stanford.edu/~cpiech/bio/papers/deepKnowledgeTracing.pdf)
* [Yudelson et al., Individualized Bayesian Knowledge Tracing Models](https://www.researchgate.net/publication/249424313_Individualized_Bayesian_Knowledge_Tracing_Models)
* [Mark Stamp, A Revealing Introduction to Hidden Markov Models](https://www.cs.sjsu.edu/~stamp/RUA/HMM.pdf)

# Data
We use the [2009-10 ASSISTments Skill-builder data](https://sites.google.com/site/assistmentsdata/home/assistment-2009-2010-data/skill-builder-data-2009-2010).

# Setting Up
1. We use the yarn package manager. Please install yarn using [these instructions](https://yarnpkg.com/lang/en/docs/install/).
2. Run `yarn` in the `WebApp` directory.
3. The `bcrypt` package requires some packages to be installed in your system. Please read the instructions on their [GitHub repo](https://github.com/pyca/bcrypt/).

# Setup
* Flask is used as the back-end web server.
* `pycodestyle` is used to lint Python code according to PEP8 guidelines.
* `run.sh` builds the Angular code, lints the Python code, and then runs the server.
* `yarn` is the package manager of choice.
