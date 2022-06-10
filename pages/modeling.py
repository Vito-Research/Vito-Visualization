import streamlit as st
import covasim as cv

# Run options
do_plot = 1
do_show = 1
verbose = 1

# Sim options
basepars = dict(
  pop_size = 2000,
  verbose = verbose,
)

# Scenario metaparameters
metapars = dict(
    n_runs    = 3, # Number of parallel runs; change to 3 for quick, 11 for real
    noise     = 0.1, # Use noise, optionally
    noisepar  = 'beta',
    rand_seed = 1,
    quantiles = {'low':0.1, 'high':0.9},
)


# Define the actual scenarios
acc = st.slider("Accuracy of Detecting Covid-19", value=77)
adherence = st.slider("% of people who quarantine after an alert", value=1)
col1, col2, col3 = st.columns(3)
mini = col1.button("Min")
mid = col2.button("Mid")
maxi = col3.button("Max")
if mini:
    acc = 77
    adherence = 1
if mid:
    acc = 77
    adherence = 10
if maxi:
    acc = 77
    adherence = 20
additionalMeasures = 0#st.slider("% of people who social distance after an alert", value=10)
if acc  != 0 and adherence != 0:
    adherence = adherence / 100
    acc = acc / 100
    total = acc * adherence
    # So it is people who do social distance 
    invereseAdditionalMeasures = 100 - additionalMeasures
    # Social distancing transmissibility * % of people who social distance
    additionalMeasures = 0.7 * (invereseAdditionalMeasures /100)
    start_day = '2020-04-04'
    scenarios = {'baseline': {
                'name':'Baseline',
                'pars': {
                    'interventions': None,
                    }
                },
                'distance': {
                'name':'Social distancing',
                'pars': {
                    'interventions': cv.change_beta(days=start_day, changes=0.7)
                    }
                },
                'ttq': {
                'name':'Test-trace-quarantine',
                'pars': {
                    'interventions': [

                            # Assuming quarantine if pos
                            cv.test_prob(start_day=start_day, symp_prob=0.2, asymp_prob=0.05, test_delay=1.0),

                            # Assuming you quarantine or get tested if you were exposed 
                            cv.contact_tracing(start_day=start_day, trace_probs=total, trace_time=1.0),
                            # cv.change_beta(days=start_day, changes=0.7)
                            # beta: The probability of transmission from an infectious person to a susceptible person, 
                            # also known as infectiousness or transmissibility. The overall transmission probability depends 
                            #on the network layer two people are connected by, as well as the infected person's viral load, 
                            #the susceptible person's age, and other factors.
                            # 0.7 social distancing ()
                            #cv.change_beta(days=start_day, changes=additionalMeasures)
                        ]
                    }
                },
                }

    

    scens = cv.Scenarios(basepars=basepars, metapars=metapars, scenarios=scenarios)
    scens.run(verbose=verbose)
    if do_plot:
        fig1 = scens.plot(do_show=do_show)
        # st.text(scens)
        st.pyplot(fig1)
        # sumer = scens.summarize()
        # 1
        if total == 0.0077:
            st.header("Min")
            st.metric("Percent Difference", value=1842.0, delta= -14.03, delta_color="inverse")
            
        # 20
        if total == 0.15400000000000003:
            st.header("Max")
            st.metric("Percent Difference", value=1481.0, delta= -35.49, delta_color="inverse")
            
        if total == 0.07700000000000001:
        # 10
            st.header("Mid")
            st.metric("Percent Difference", value=1674.0, delta= -23.5, delta_color="inverse")