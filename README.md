# Why_is_episodic_memory_fuzzy
A mathematical explanation for why the temporal coding in episodic memory is fuzzy with experimental verification across brain regions and animal species.

<div align="center">

**Abstract**

</div>
The temporal representation of episodic memory is supported by ramping cell in the entorhinal cortex and time cell population in the hippocampus. While we know that we have a fuzzy memory about the ”when” of the events happened in the past, a math- ematical explanation for why the episodic memory is fuzzy is lacking. Here, we view the problem of episodic memory retrieval as an inverse problem with an biologically plausible encoder that encodes the stimulus history and do not specify the decoder. Through the language of spectral operator theory, we find that the exact inverse con- structed from the intermediate representation produced by the encoder is unbounded. We attribute the fuzziness in the temporal representation of past experience to the decaying singular values of the encoder. Further numerical analysis shows that this inverse problem is an severely ill-posed and offer an approach of reconstructing past stimulus history through predictive coding.



This github repository contains the code and data for the paper "Why is episodic memory fuzzy? - A mathematical explanation". While the experimental data are obtained from the following four papers:
- [Ramping cells in the rodent medial prefrontal cortex encode time to past and future events via real Laplace transform
](https://www.pnas.org/doi/10.1073/pnas.2404169121)
- [Distributed coding of duration in rodent prefrontal cortex during time reproduction](https://elifesciences.org/articles/71612)
- [A temporal record of the past with a spectrum of time constants in the monkey entorhinal cortex](https://www.pnas.org/doi/10.1073/pnas.1917197117#fig02)
- [Integrating time from experience in the lateral entorhinal cortex](https://www.nature.com/articles/s41586-018-0459-6#ref-CR31)

We only put the dataset here that are available to download from the internet and we appreciate the dataset shared from the corresponding author in the paper [Integrating time from experience in the lateral entorhinal cortex](https://www.nature.com/articles/s41586-018-0459-6#ref-CR31) (Albert Tsao & Edvard I. Moser). However, the dataset availability statement in that paper is to ask the corresponding author to provide the data. Therefore, we don't put the data her. 

The link for Cao data (we download the past cells): [link](https://osf.io/rkxps/overview)

The link for Bright data (we use the temporal context cell they found in their paper using the first column of finalparameters.csv): [link](https://github.com/tcnlab/TemporalContextCells-ECmonkey)

The code for downloading this github repository is:
```
git clone https://github.com/III-Derek/Why_is_episodic_memory_fuzzy
```
