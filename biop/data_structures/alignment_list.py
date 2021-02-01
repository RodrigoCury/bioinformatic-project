class Alignment():
    def __init__(self, seq1: str, align: str, seq2: str, score: int, start: int, end: int):
        self._seq1 = seq1
        self._seq2 = seq2
        self._score = score
        self._align = align
        self._start = start
        self._end = end

    @property
    def seq1(self):
        return self._seq1

    @property
    def seq2(self):
        return self._seq2

    @property
    def align(self):
        return self._align

    @property
    def score(self):
        return self._score

    def __lt__(self, o: object) -> bool:
        return self._score < o.score

    def __le__(self, o: object) -> bool:
        return self._score <= o.score

    def __eq__(self, o: object) -> bool:
        return self._score == o.score

    def __ne__(self, o: object) -> bool:
        return self._score != o.score

    def __gt__(self, o: object) -> bool:
        return self._score > o.score

    def __ge__(self, o: object) -> bool:
        return self._score >= o.score

    def __repr__(self):
        return self._seq1 + "\n" + self._align + "\n" + self._seq2 + "\n"

    def __str__(self):
        return str(self._score)
        # return self._seq1 + "\n" + self._align + "\n" + self._seq2 + "\n"


class PriorityQueue():

    def __init__(self):
        self._pq = []
        self._len = 0

    @property
    def pq(self):
        return self._pq

    @property
    def len(self):
        return self._len

    def isEmpty(self):
        if self._len == 0:
            return True
        return False

    def addOne(self):
        self._len += 1

    def delOne(self):
        self._len -= 1

    def __str__(self):
        for i in self.pq:
            print(i)
        return "\n"

    def __len__(self):
        return self._len

    # inserts on a priority decreasingly ordered fashion
    def push(self, alignment):
        # error first
        if not isinstance(alignment, Alignment):
            print(
                f"To insert {alignment} must be an instance of Alignment Class")
        else:
            if self.isEmpty():
                self.pq.append(alignment)
                self.addOne()
            else:

                flag_push = False

                # search for the right priority
                for index in range(self.len):
                    if self.pq[index] <= alignment:
                        self._pq.insert(index, alignment)
                        flag_push = True
                        break

                if not flag_push:
                    self._pq.append(alignment)

                self.addOne()

    def pop(self):
        self._pq.pop()
        self.delOne()

    @staticmethod
    def convert_to_list(alignments):
        alignments_list = PriorityQueue()
        for alignment in alignments:
            formatted = format_alignment(*alignment).split("\n")[:3]
            seq1, align, seq2 = formatted
            a = Alignment(seq1, align, seq2, alignment.score,
                          alignment.start, alignment.end)
            alignments_list.push(a)
        return alignments_list

    def __getitem__(self, index):
        return self._pq[index]
