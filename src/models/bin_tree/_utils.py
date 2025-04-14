class BinaryTree:
    
    # TODO: change args to mu and sigma and auto convert to tree form with up/down factor
    def __init__(self, stock_value = None, deriv_value = None):
        assert stock_value >= 0, "stock cannot have negative value"

        self.up  = None
        self.done = None
        self.stock_value = stock_value
        self.deriv_value = deriv_value


    def grow_tree(self, depth, u, d):
        """
        Grows a binary tree from the root node. Uses root node's self.stock_value and up and down factor to calculate stock_value at each node. 
        """

        assert (depth > 0) and (u > d) and (d > 0), f"invalid parameters passed \n depth:{depth}, u:{u}, d:{d}"

        self.u = u
        self.d = d

        self.up = BinaryTree(self.stock_value*u)
        self.down = BinaryTree(self.stock_value*d)

        if depth > 1:
            self.up.grow_tree(depth - 1, u, d)
            self.down.grow_tree(depth - 1, u , d)


    def fill_deriv_terminal(self, terminal_values): 
        """
        Fills the end of the tree with the terminal values of the derivative security
        
        Careful that terminal_values is of correct length. Will return empty list if you passed correct length list
        """

        if self.is_terminal():
            self.deriv_value = terminal_values[0]
            return terminal_values[1:]
        else:
            terminal_values = self.up.fill_deriv_terminal(terminal_values)
            terminal_values = self.down.fill_deriv_terminal(terminal_values)
            return terminal_values


    def fill_deriv_latent(self, rate = 0):
        """
        
        """
        if self.up.deriv_value is None:
            self.up.fill_deriv_latent(rate)

        if self.down.deriv_value is None:
            self.down.fill_deriv_latent(rate)

        self.deriv_value = self.calc_node_deriv_value(rate)


    def fill_deriv(self, terminal_values, rate = 0):
        self.fill_deriv_terminal(terminal_values)
        self.fill_deriv_latent(rate)


    def calc_node_deriv_value(self, rate):
        """
        """
        delta = (self.up.deriv_value - self.down.deriv_value)/(self.up.stock_value - self.down.stock_value)

        gamma = (self.up.deriv_value - (delta*self.up.stock_value))/(1+rate)

        self.delta = delta
        self.gamma = gamma

        return (delta*self.stock_value) + gamma
    
    def get_terminal_values(self, get_stock = True):
        if self.is_terminal():
            if get_stock: return [self.stock_value]
            else: return [self.deriv_value]
        else:
            return self.up.get_terminal_values(get_stock) + self.down.get_terminal_values(get_stock)


    def print_node(self):
        print(f"underl: {self.stock_value}  \nderiva: {self.deriv_value} ")


    def is_terminal(self):
        return self.up == None 
    

