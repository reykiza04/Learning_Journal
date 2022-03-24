from datetime import datetime
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.figure_factory as ff

np.random.seed(42)


def hypothesis_testing_ui(df: pd.DataFrame):
    st.markdown("# Hypothesis Testing")

    alpha = 0.05

    st.markdown(f"""
    > ## Hypothesis
    >> The null hypothesis is that the population mean is equal to the value of the variable of interest.  
    >> The alternative hypothesis is that the population mean is not equal to the value of the variable of interest.  
    >>  
    >> μ1 = `Male` Customer Spending on `Health and Beauty` Product  
    >> μ2 = `Female` Customer Spending on `Health and Beauty` Product 
    >>
    >>> ### Null and Alternate Hypothesis  
    >>> H0 : μ1 = μ2  
    >>> H1 : μ1 ≠ μ2
    >>> ### Significance Level
    >>> The significance level is the probability of observing the null hypothesis if the null hypothesis is true.  
    >>>  
    >>> α = {alpha:.2f}  
    >>> ### Assumptions
    >>> μ1 and μ2 are normally distributed.  
    > ## Test Statistic
    >> The test statistic is the difference between the population mean and the value of the variable of interest.  
    """)

    col1, col2 = st.columns(2)

    df = df[df.product_line == "Health and beauty"]
    male_df = df[df.gender == "Male"]
    female_df = df[df.gender == "Female"]

    col1.markdown("## Male Spending")
    col2.markdown("## Female Spending")

    col1.markdown("""
    > From this data we can calculate the `mean` and `standard deviation` for each group and then we can create rew normal distribution with
    > that property to create sample for T-Test
    """)

    fig, ax = plt.subplots(1, 2, figsize=(24, 6), sharex=True, sharey=True)
    ax[0].set_title("Male Spending")
    ax[0].hist(male_df.total, bins=8)

    ax[1].set_title("Female Spending")
    ax[1].hist(female_df.total, bins=8)
    # st.pyplot(fig)

    col1, col2 = st.columns(2)
    col1.plotly_chart(ff.create_distplot([female_df.total.values], ["Test"], curve_type='kde', bin_size=32), use_container_width=True)
    col2.plotly_chart(px.histogram(female_df.total), use_container_width=True)

    st.markdown("""
        > After re-sampling from normal distribution we see that `Central Tendency` of our sample is mimicking our original distribution
    """)

    _sample_male_mean = male_df.total.mean()
    _sample_male_std = male_df.total.std()
    _sample_female_mean = female_df.total.mean()
    _sample_female_std = female_df.total.std()

    male_sample = np.random.normal(_sample_male_mean, _sample_male_std, size=512)
    female_sample = np.random.normal(_sample_female_mean, _sample_female_std, size=512)

    col1.plotly_chart(ff.create_distplot([male_sample], ["Test"], curve_type='kde', bin_size=32), use_container_width=True)

    fig, ax = plt.subplots(1, 2, figsize=(24, 6), sharey=True, sharex=True)
    ax[0].set_title("Distribution of Male Sample")
    ax[0].hist(male_sample, bins=64)

    ax[0].axvline(_sample_male_mean, linestyle="--", color='r', label="Mean")
    ax[0].axvline(np.median(male_sample), linestyle="--", color='c', label="Median")
    ax[0].axvline(_sample_male_mean + _sample_male_std, linestyle="--", color='g', label="Deviation")
    ax[0].axvline(_sample_male_mean - _sample_male_std, linestyle="--", color='g')

    ax[0].axvline(_sample_male_mean + _sample_male_std * 2, linestyle="--", color='y', label="2x Deviation")
    ax[0].axvline(_sample_male_mean - _sample_male_std * 2, linestyle="--", color='y')

    ax[0].legend()

    ax[1].set_title("Distribution of Female Sample")
    ax[1].hist(female_sample, bins=64)

    ax[1].axvline(_sample_female_mean, linestyle="--", color='r', label="Mean")
    ax[1].axvline(np.median(female_sample), linestyle="--", color='c', label="Median")
    ax[1].axvline(_sample_female_mean + _sample_female_std, linestyle="--", color='g', label="Deviation")
    ax[1].axvline(_sample_female_mean - _sample_female_std, linestyle="--", color='g')

    ax[1].axvline(_sample_female_mean + _sample_female_std * 2, linestyle="--", color='y', label="2x Deviation")
    ax[1].axvline(_sample_female_mean - _sample_female_std * 2, linestyle="--", color='y')

    ax[1].legend()
    st.pyplot(fig)

    st.markdown("# Confidence Interval Visualisation")

    male_sample = pd.Series(male_sample)
    female_sample = pd.Series(female_sample)

    fig, ax = plt.subplots(figsize=(8 * 3, 8))
    ax.set_title("Male vs Female Spending on Health and beauty")
    ax.hist(male_sample, histtype='step', density=True, bins=64, color="blue")
    ax.hist(female_sample, histtype='step', density=True, bins=64, color="red")

    male_sample.plot.kde(ax=ax, label="Male Spending", color="blue")
    female_sample.plot.kde(ax=ax, label="Female Spending", color="red")

    lower_confidence, upper_confidence = stats.norm.interval(1 - alpha, loc=_sample_male_mean, scale=_sample_male_std)
    t_statistic, p_value = stats.ttest_ind(male_sample, female_sample)

    ax.axvline(x=lower_confidence, color="g", linestyle="--", label="Confidence Interval")
    ax.axvline(x=upper_confidence, color="g", linestyle="--")

    ax.axvline(x=_sample_male_mean + t_statistic * _sample_male_std, color="k", linestyle="--", label="Alternate Hypothesis")
    ax.axvline(x=_sample_male_mean - t_statistic * _sample_male_std, color="k", linestyle="--")
    ax.legend()
    st.pyplot(fig)

    st.markdown(f"""
    # Conclusion
    > ## Statistic Discovery
    >> The test statistic is `{t_statistic:.2f}`  
    >> The p-value is `{p_value:.2f}`  
    >>  
    >> From the p-value, we can conclude that the null hypothesis is `{'Invalid' if p_value < alpha else 'Valid'}` with a probability of `{(1 - p_value) * 100:.1f}%`  
    >>  
    >> ### Summary  
    >> We will **{'`Reject Null Hypothesis` because there are' if (p_value < alpha)
    else '`Not Reject Null Hypothesis` because there are no'} significant difference between variable**
    """)
