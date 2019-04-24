import numpy as np


class AdaptiveTester:
    """
    A simple adaptive testing module. Works by first checking for
    items that haven't been administered yet, and administers them
    first. Next, checks for items with highest error rate.
    """
    def __init__(self, item_count: int, administered: list, responses: list,
                 bucket_size=10, debug=False):
        """
        Initializes the module.

        Args:
        =====
        item_count: int. Total count of items in the database.
        administered: list. Each item is an INDEX of the administered item.
        responses: list. Each item is a BOOLEAN, whether the corresponding
                   administered item was answered correctly or not.
        bucket_size: int. The bucket size to use.
        """
        if len(administered) != len(responses):
            raise ValueError('Length of administered and response arrays must \
                be the same.')

        if bucket_size < 1:
            raise ValueError('bucket_size must be at least 1.')

        self.item_count = item_count
        self.administered = np.array(administered)
        self.responses = np.array(responses)
        self.bucket_size = bucket_size
        self.debug = debug

        if debug:
            print('Administered:', self.administered)
            print('Responses:', self.responses)

    def get_next_question(self):
        # Go over each bucket
        for i in range(self.item_count // self.bucket_size + 1):
            # Get the bucket index limits: (0..9), (10..19), and so on.
            bucket_start = i * self.bucket_size
            bucket_end = min((i + 1) * self.bucket_size - 1, self.item_count)

            index_range = set(range(bucket_start, bucket_end + 1))
            uniq_administered = set(self.administered)

            if self.debug:
                print('Index range:', index_range)

            if index_range.issubset(uniq_administered):
                # All items in this bucket have been administered. Now check
                # for items that have been answered wrongly, but NOT answered
                # correctly in a later attempt.
                #
                # First, convert back to lists.
                index_range = list(index_range)

                # Iterate over the current bucket
                for item in index_range:
                    # Grab the last index where item was seen.
                    # This index is the actual array index, and has nothing to
                    # do with the item indices.
                    last_seen_index = np.where(
                        self.administered == item)[0][-1]

                    if self.debug:
                        print('Last seen index for', item, 'is', 
                              last_seen_index)

                    if not self.responses[last_seen_index]:
                        if self.debug:
                            print('Choosing item')
                        return item
            else:
                # This case is easy: administer the first unadministered item.
                sorted_bucket = sorted(list(index_range))
                for index in sorted_bucket:
                    if index not in self.administered:
                        return index

        # If we've come here, all items have been administered, and
        # all mistakes were corrected.
        return np.random.randint(0, self.item_count)
