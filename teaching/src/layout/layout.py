class Layout:
    def __init__(self, nranks, shape, gbl_shape):
        self.shape = shape
        self.nranks = nranks
        self.gbl_shape = gbl_shape
        ranks_per_edge = []
        for dim, (edge, gbl_edge) in enumerate(zip(self.shape, self.gbl_shape)):
            ratio = gbl_edge // edge
            assert ratio >= 1, f'for dim {dim}, edge length {edge} is wider than global edge length {gbl_edge}'
            assert ratio * edge == gbl_edge, f'for dim {dim}, global edge length {gbl_edge} is not a multiple of edge {edge}'
            ranks_per_edge.append(ratio)
        check_ranks = 1
        for rank in ranks_per_edge:
            check_ranks *= rank
        #print(ranks_per_edge)
        assert check_ranks == self.nranks, f'The layout requires {check_ranks} ranks but there are {self.nranks}'
        self.ranks_per_edge = ranks_per_edge
    def gbl_to_lcl(self, gbl_indices):
        """
        Returns a tuple (rank, (lcl_indices)) giving the rank and local indices of the given global location
        """
        rank_offsets = []
        block_offsets = []
        for dim, (gbl_index, ranks_this_edge, edge) in enumerate(zip(gbl_indices, self.ranks_per_edge, self.shape)):
            assert gbl_index >= 0, f'cannot map negative index {gbl_index}'
            rank = gbl_index // edge
            assert rank < ranks_this_edge, f'index {gbl_index} is out of range for dimension {dim}'
            offset = gbl_index - (rank * edge)
            rank_offsets.append(rank)
            block_offsets.append(offset)
        #print(rank_offsets, block_offsets)
        gbl_rank = 0
        scale = 1
        for rank, ranks_this_edge in zip(reversed(rank_offsets), reversed(self.ranks_per_edge)):
            gbl_rank += rank * scale
            scale *= ranks_this_edge
            #print(rank, ranks_this_edge, gbl_rank, scale)
        return gbl_rank, tuple(block_offsets)
    def lcl_to_gbl(self, this_rank, indices):
        gbl_rank = 0
        rank_remainder = this_rank
        rank_offsets = []
        for dim, ranks_this_edge in enumerate(reversed(self.ranks_per_edge)):
            #print(f'{rank_remainder} ->')
            this_offset = rank_remainder % ranks_this_edge
            rank_remainder //= ranks_this_edge
            rank_offsets.append(this_offset)
            #print(dim, ranks_this_edge, this_offset, rank_remainder)
        rank_offsets = reversed(rank_offsets)
        #print([r for r in rank_offsets])  # or else we just print the iterator object
        gbl_indices = []
        #print('-------------------')
        for this_offset, this_index, edge in zip(rank_offsets, indices, self.shape):
            gbl_indices.append(this_offset * edge + this_index)
            #print(f'{this_offset}, {this_index}, {edge} -> gbl_indices[-1]')
        #print(gbl_indices)
        return(gbl_indices)
