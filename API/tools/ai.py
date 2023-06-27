
from pandas import DataFrame
from numpy import log, ones, array, transpose, matmul, exp
from scipy.optimize import minimize


class OptimalPortfolio():
    
    '''
    
    asset_information_dataframe : DataFrame witn information about financial assets.
    it has to contain assets names as titles of columns, datetime information as index and
    price per time of each asset in the cell
    
    index          asset1          assse2           ..........         asset-n
    
   datetime 1    price(1,1)      price(1,2)         ..........        price(1,n)
    
    ...          .........       .........          ..........        .........
    
    ...          .........       .........          ..........        .........
    
    ...          .........       .........          ..........        .........
    
  dateime n    price(m,1)      price(m,2)          ..........       price(m,n) 
    
    
    '''
    
    
    def __init__(
            self,
            asset_information_dataframe = DataFrame(),
            shortable =  False
            ):
        
        
        self.price_information = asset_information_dataframe
        
        
        err_msg = '''
            The DataFrame can´t have null values
        '''
        
        assert not self.price_information.isnull().values.any() , err_msg
        
        err_msg = '''
            for correct specification in the model, the information dataframe need
            to have more information about prices than the number of assets.
            this condition is to fulfill the random sampling asumption
        '''
        
        assert self.price_information.shape[0] > self.price_information.shape[1], err_msg
        
        err_msg = '''
            is required information at least for one asset to estimate the optimal participation
        '''
        
        assert self.price_information.shape[1] > 0, err_msg
        
        
        
        
        self.asset_names = self.price_information.columns.tolist()
        
        self.DLP_information = DataFrame()
        
        for asset in self.asset_names:
            
            self.DLP_information[asset] = self.price_information[asset].apply(
                lambda x: log(x)
                )
            
            self.DLP_information[asset] = self.DLP_information[asset].diff()
        
        self.mean_vector = self.DLP_information.mean().values
        self.std_vector = self.DLP_information.std().values
        
        self.covariance_matrix = self.DLP_information.cov().values
        
        self.ones_vector = ones(
            len(self.asset_names),
            dtype=int
            )
        
        self.number_assets = len(self.asset_names)
        
        self.initial_point = [1/self.number_assets for _ in self.asset_names]
        
        if shortable:
            self.bounds = [(-1,1) for _ in self.asset_names]        
        else:
            self.bounds = [(0,1) for _ in self.asset_names]

    def constraint(self,
                   coeffients_vector
                   ):
        coeffients_vector = array(
            [coeffients_vector]
            )
    
        sum_coefficients = matmul(
            coeffients_vector,
            transpose(
                self.ones_vector
                )
            )
        sum_coefficients = sum_coefficients[0]
        
        return sum_coefficients - 1
    
    def expected_return(self,
                        coeffients_vector
                        ):

        ln_portfolio_growth = matmul(
            coeffients_vector,
            transpose(
                self.mean_vector
                )
            )
        
        #ln_portfolio_growth = ln_portfolio_growth[0][0]
        
        portfolio_growth = exp(
            ln_portfolio_growth
            )
        
        portfolio_growth -= 1
        
        return portfolio_growth
    
    def variance_return(self,
                        coefficients_vector
                        ):
       ln_Portf_growth_var =  matmul(
           matmul(
               coefficients_vector,
               self.covariance_matrix
               ),
           transpose(
               coefficients_vector
               )
           )
       #ln_Portf_growth_var = ln_Portf_growth_var[0][0]
       
       Portf_growth_var = exp(
           ln_Portf_growth_var
           )
       
       Portf_growth_var -= 1
       
       return Portf_growth_var

    def std_return(self,
                    coefficients_vector
                    ):

        portfolio_variance = self.variance_return(
            coefficients_vector
            )        
       
        portfolio_std = (portfolio_variance + 1)**(1/2)
        
        portfolio_std -= 1
        
        return portfolio_std
        
    def objective_equation(self,
                           coefficients_vector
                           ):

        coefficients_vector = array(
            [coefficients_vector]
            )

        portfolio_growth = self.expected_return(
            coefficients_vector
            )
        
        
        portfolio_std = self.std_return(
            coefficients_vector
            )

        objective_result = portfolio_std / portfolio_growth    
        
        return objective_result[0][0]
        
    
    def optimize(self):
        if self.number_assets == 1:
             self.optimal_point = [1]
            
        else:
            self.solution = minimize(
                self.objective_equation,
                self.initial_point,
                method = 'SLSQP',
                bounds = self.bounds,
                constraints = [
                    {
                        'type':'eq',
                        'fun' : self.constraint
                        }
                    ]
                )
            
            self.optimal_point = self.solution.x.tolist()
            
        
        return self.optimal_point
