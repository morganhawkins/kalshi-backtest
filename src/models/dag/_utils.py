class DAG:
    """
    Very similar to binary tree model, but here our up_factor*down_factor = 1 so that our tree is actually a direct acyclic graph where nodes in the 
    same depth that are adjacent point to a common child
            *
        *
    *       *
        *   
            *
    """

    # TODO: change args to mu and sigma and auto convert to tree form with up/down factor
    def __init__(self, stock_value: float = None, deriv_value: float = None):
        assert stock_value >= 0, "stock cannot have negative value"

        self.up = None
        self.down = None
        self.stock_value = stock_value
        self.deriv_value = deriv_value

    def grow_tree(self, depth, u):
        d = 1/u
        assert (depth > 0) and (u > 1), "invalid parameters passed"

        if self.up == None:
            self.up = DAG(stock_value=self.stock_value*u)

        if self.down == None:
            self.down = DAG(stock_value=self.stock_value*d)

        if depth > 1:
            forward_child = DAG(stock_value=self.stock_value)
            self.up.down = forward_child
            self.down.up = forward_child

            self.up.grow_tree(depth=depth - 1, u=u)
            self.down.grow_tree(depth=depth - 1, u=u)

    def is_terminal(self):
        no_up = self.up == None
        no_down = self.down == None

        # assert not (no_up ^ no_down), "node has only 1 child, check DAG construction" #checks that the node is

        return no_up

    def depth(self):
        """
        returns the number of additional levels after the node from which function called
        """
        if self.is_terminal():
            return 0
        else:
            return 1 + self.up.depth()

    def get_terminal_values(self, get_stock=True):

        depth = self.depth()
        # print(depth,"\n\n")

        term_vals = []

        for downs in range(depth + 1):
            current_node = self
            # print(downs)

            for _ in range(downs):
                # print("down")
                current_node = current_node.down

            for _ in range(depth - downs):
                # print("up")
                current_node = current_node.up

            # print("\n")

            if get_stock:
                term_vals.append(current_node.stock_value)
            else:
                term_vals.append(current_node.deriv_value)

        return term_vals

    def calc_node_deriv_value(self, rate):
        """
        """
        delta = (self.up.deriv_value - self.down.deriv_value) / \
            (self.up.stock_value - self.down.stock_value)

        gamma = (self.up.deriv_value - (delta*self.up.stock_value))/(1+rate)

        self.delta = delta
        self.gamma = gamma

        return (delta*self.stock_value) + gamma

    def fill_deriv_terminal(self, terminal_vals):
        """
        Fills the end of the tree with the terminal values of the derivative security

        Careful that terminal_values is of correct length. Will return empty list if you passed correct length list
        """

        depth = self.depth()

        for ups in range(depth + 1):
            current_node = self

            for _ in range(ups):
                current_node = current_node.up

            for _ in range(depth - ups):
                current_node = current_node.down

            # print("\n")

            current_node.deriv_value = terminal_vals.pop()

    def fill_deriv_latent(self, rate=0):
        """

        """
        if self.up.deriv_value is None:
            self.up.fill_deriv_latent(rate)

        if self.down.deriv_value is None:
            self.down.fill_deriv_latent(rate)

        self.deriv_value = self.calc_node_deriv_value(rate)

    def fill_deriv(self, terminal_vals, rate=0):
        self.fill_deriv_terminal(terminal_vals)
        self.fill_deriv_latent(rate)

    def print_node(self):
        print(
            f"""
            stock val: {round(self.stock_value, 4)}
            deriv val: {round(self.deriv_value, 4)}
            node delta: {round(self.delta, 4)}
            node gamma: {round(self.gamma, 4)}"""
        )


def _build_tree(
    u_price: float,
    strike: float,
    u,
    depth: int
) -> DAG:
    # init dag
    dag = DAG(stock_value=u_price)

    # fill underlying values
    dag.grow_tree(depth, u)

    # get terminal underlying values and determine deriv cf
    under_term = dag.get_terminal_values(get_stock=True)
    deriv_term = [p > strike for p in under_term]

    # fill terminal_deriv_values and check that correct number of items were passed
    leftover = dag.fill_deriv_terminal(deriv_term)
    if leftover:
        raise Exception("Unexpected error in _build_treee. number "
                        "of terminal values != number of terminal nodes")

    # filling in intermediate nodes delta, gamma, and value
    dag.fill_deriv_latent(rate=0)

    return dag
