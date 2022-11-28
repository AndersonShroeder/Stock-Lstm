# Stock Prediction Effectiveness
<h2>1 - Data Preperation</h2>
<h3>1.1 - Importing Data/Libraries</h3>
<p>We begin by importing the necessary libraries and the following classes:</p>
<ul>
<li>The Analyzer Class: </li>
<p>This class contains all necessary data and methods to operate on and prepare the data to be utilized within the LSTM/Markov models.
 The class also contains methods to visualize data.</p>
<li>The LSTM Class: </li>
<p>This class contains all necessary data and methods to create and fit an LSTM network with varying amounts of inputs and timesteps. To train an LSTM network, an
instance of this class must be created and then the divide_data method must be called, followed by the run method. This class also contains methods to visualize the data
and generate future predictions.</p>
<li>The Markov Class: </li>
<p>This class contains all necessary data and methods to create and optimize a Markov chain with varying degrees. In order to run and train a Markov chain model
an instance of this class must be created and then the optimal_degree method must be utilized.</p>
</ul>
<h3>1.2 - Preparing The Subreddit Sentiment Data </h3>
<p>We now group all data points in the Subreddit Sentiment data by the day on which they occured. </p>
<h3>1.3 - Preparing The Stock Price Data</h3>
<p>We now group all data points in the Stock data by the day on which they occured.  </p>
<h3>1.4 - Merging The Sentiment Data And Stock Price Data</h3>
<p>Now the two dataframe are merged to form the complete dataframe. </p>
<h3>1.5 - Determining Percent Change In Price</h3>
<p>We Now find the percent chagne which can be done by subtracting the prices column by the prices column shifted down one. </p>
<h2>2 - Visualizing Trends In News Sentiment and Stock Prices</h2>
<h3>2.1 - Plotting Sentiment Versus Price</h3>
![](images/output.png)
<h2>3 - Markov Chains</h2>
<h3>3.1 - Plotting Hist</h3>
<h3>3.2 - Nth Degree Markov Chains<h3>
<h3>3.3 - Optimizing Nth Degree Markov Chains<h3>
<h2>4 - Univariate LSTM Network</h2>
<h3>4.1 - Processing And Splititng Data</h3>
<h3>4.2 - Fitting The Model</h3>
<h3>4.3 - Plotting True And Predicted Values</h3>
<h3>4.4 - Comparing n Values</h3>
<h2>5 - Multivariate LSTM Network Using Reddit News Sentiments</h2>
<h3>5.1 - Processing And Splitting Data </h3>
<h3>5.2 - Fitting The Model </h3>
<h3>5.3 - Plotting True And Predicted Values </h3>
<h3>5.4 - Prediction Of Future Values </h3>
