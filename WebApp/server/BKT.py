from hmmlearn.hmm import MultinomialHMM


class BKT:
    """
    Implements the Bayesian Knowledge Tracing model. This only
    implements the Viterbi and EM algorithms. These may be used
    together to implement an Intelligent Tutoring System.
    """
    def __init__(self, observed):
        """
        Initializes the object and sets the internal state.

        Args:
            observed: array-like, shape (n_samples, n_features)
        """
        self.observed = observed
        # TODO: Check other parameters to this constructor
        self.model = MultinomialHMM(n_components=2)

    def fit(self):
        """
        Fits the model to the observed states. Uses the EM algorithm
        to estimate model parameters.
        """
        self.model.fit(self.observed)

    def get_model_params(self):
        """
        Returns the model parameters. This must be run only after
        calling the `fit` function.

        Returns:
            (A, pi, B): The start probabilities, the transition
                        probabilities, and the emission probabilities.
        """
        return self.model.startprob_, self.model.transmat_, \
            self.model.emissionprob_
