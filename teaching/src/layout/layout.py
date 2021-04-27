import numpy as np

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
        gbl_indices = gbl_indices % np.array(self.gbl_shape)  # wrap everything back to the actual range
        gbl_offset = np.ravel_multi_index(gbl_indices, self.gbl_shape)
        long_shape = np.array([pair for pair in zip(self.ranks_per_edge, self.shape)]).flatten()
        long_indices = np.unravel_index(gbl_offset, long_shape)
        long_index_array = np.array(long_indices).reshape((-1,2))
        #print('long_index_array follows')
        #print(long_index_array)
        gbl_rank = np.ravel_multi_index(long_index_array[:, 0], self.ranks_per_edge)
        return gbl_rank, long_index_array[:, 1]
    def get_rank_indices(self, this_rank):
        return np.unravel_index(this_rank, self.ranks_per_edge)
    def lcl_to_gbl(self, this_rank, indices):
        rank_offsets = self.get_rank_indices(this_rank)
        return(rank_offsets * np.array(self.shape) + np.array(indices))
    def fill_with_gbl_addr(self, rank, target):
        assert target.shape == self.shape, 'target of fill_with_global_address is the wrong shape'
        assert rank in range(self.nranks), 'rank is out of range'
        assert len(self.shape) == 3, "This routine only supports 3D local arrays"
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                #print(i,j)
                index_l = [(i, j, k) for k in range(self.shape[2])]
                #print(index_l)
                gbl_idx_l = self.lcl_to_gbl(rank, index_l)
                #print(gbl_idx_l)
                gbl_addr_l = np.ravel_multi_index(gbl_idx_l.T, self.gbl_shape)
                #print(gbl_addr_l)
                target[i, j, :] = np.array(gbl_addr_l)
                #print('done')
        return target
