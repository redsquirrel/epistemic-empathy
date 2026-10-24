# Related work and novelty boundaries

Initial reading list checked 2026-10-24. These are primary-source starting points,
not a systematic review. Summaries below are limited to the abstracts and source
pages consulted. Read full methods and instruments before adopting measures or
making detailed comparisons. No benchmark data or questionnaire items are copied.

- **Sharma et al., Towards Understanding Sycophancy in Language Models.**
  [arXiv:2310.13548v4](https://arxiv.org/abs/2310.13548v4).
  Studies agreement with user beliefs and the potential role of preference
  judgments. Motivates separating user-pleasing validation from warranted claims.
  It does not validate this project's empathy rubric.
- **Kim et al., FANToM: A Benchmark for Stress-testing Machine Theory of Mind in
  Interactions (EMNLP 2023).**
  [ACL Anthology](https://aclanthology.org/2023.emnlp-main.890/).
  Evaluates perspective reasoning in information-asymmetric conversational
  contexts. Motivates explicit control over who has access to which information.
  Our fixtures instead expose different narratives to the evaluated model; they
  do not yet implement FANToM-style belief-access reasoning or interactive tasks.
- **Kadavath et al., Language Models (Mostly) Know What They Know.**
  [arXiv:2207.05221v4](https://arxiv.org/abs/2207.05221v4).
  Studies model self-evaluation and uncertainty, including limitations in
  generalizing calibration. Motivates measuring probabilities rather than merely
  counting hedging phrases. Our probabilities concern evidence-status labels,
  not the probability of knowing an answer as operationalized in that work.
- **Cheng et al., Sycophantic AI Decreases Prosocial Intentions and Promotes
  Dependence.** [2025 preprint v1](https://arxiv.org/abs/2510.01395v1);
  [later Science publication](https://doi.org/10.1126/science.aec8352).
  Studies interpersonal sycophancy and human responses. The preprint abstract
  reports experiments linking sycophantic interaction to reduced willingness to
  repair conflict. This project does not reproduce those human-outcome studies;
  fictional text scores cannot establish comparable effects. Cite the exact
  version when discussing methods because the preprint and publication differ.
- **Rehani et al., The Social Sycophancy Scale: A psychometrically validated
  measure of sycophancy.**
  [arXiv:2603.15448v1](https://arxiv.org/abs/2603.15448v1).
  Proposes a behavioral measure spanning uncritical agreement, obsequiousness,
  and excitement. Its abstract describes empirical validation; our custom rubric
  has none yet. Review its full instrument and reuse terms before deciding
  whether to use it as a complementary outcome.

Candidate contribution: an openly auditable paired-narrative protocol separating
emotional acknowledgment, evidence-status uncertainty, and unsupported attribution.
This is a **hypothesis about a useful measurement design**, not an established gap
in the literature. Before claiming novelty, compare full methods, existing social
sycophancy instruments, perspective benchmarks, and related epistemic-empathy
constructs; invite critique from researchers with relevant expertise.
