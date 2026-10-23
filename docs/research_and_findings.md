# Airline Revenue Management MVP — Critical Review of Four Foundation Papers

**Prepared:** 21 October 2026  
**Scope:** All 46 pages across four user-provided PDFs (17 + 10 + 7 + 12).  
**Purpose:** Assess technical and scientific fit for Skytech's single-leg, recommendation-only airline pricing MVP and identify what to implement and validate next.  
**Evidence status:** Page references below are **PDF page numbers** (not necessarily journal page numbers). The authors' quantitative results describe **their study settings**, not expected uplift for Skytech.

## Executive assessment

**Keep the architecture, but distinguish four engineering processes:** (1) transactional and operational data preparation, (2) baseline demand forecasting and unconstraining when supported by availability history, (3) causal / conditional price response estimation, and (4) capacity-aware decision optimization with a human-in-the-loop guardrail. Add a fifth, explicit process for offline evaluation and online monitoring.

The current Python MVP **does** contain a usable historical-fare summary, scenario-based constant-elasticity function, capacity-capped grid search, and Streamlit interface. It **does not yet** implement the algorithms developed in the four studies, estimate true demand, validate price elasticity, forecast future bookings from airline booking curves, or demonstrate real airline revenue uplift. The $169.76 historical market median is sourced from BTS DB1C; the 60-booking baseline, -1.2 elasticity, and 45 available seats are scenario assumptions. Preserve these distinctions in any presentation.

## Paper 1. Mumbower, Garrow & Higgins (2014)
**Estimating flight-level price elasticities using online airline data: A first step toward integrating pricing, demand, and revenue optimization.** Transportation Research Part A, 66, 196–212. 17 PDF pages.

### All-page reading map
- **Pages 1–2:** Motivation. Traditional RM forecasting by booking class is not equivalent to forecasting quantity demanded as a function of a price intervention. More fine-grained fare and competitor observations are necessary; aggregated O&D fares are insufficient for day-to-day flight pricing.
- **Pages 3–4:** Data and identification context. Four transcontinental JetBlue markets, 13 flight numbers, 21 departure dates, 28-day booking windows; daily prices and seat maps gathered from consumer-facing websites. A new booking is *approximated* from a seat changing from available to reserved. Authors note this is not identical to observed customer demand; consumer airline choice and seat selection can cause selection bias. They choose mostly nonstop/local itineraries, largely setting network RM aside.
- **Page 5:** Variables: daily flight bookings, fare, days to departure (DFD), booking and departure weekdays, departure time, holidays, competitor promotions, market indicators, and two proposed instruments. The paper models *flight-day booking counts*, not BTS-style monthly ticket-row totals.
- **Pages 5–6:** Estimation strategy. Missing online observations addressed via inverse probability weighting. Compare OLS demand regression with instrumental-variable two-stage least squares (2SLS), controlling for price endogeneity; apply clustered, robust inference.
- **Pages 6–8:** Candidate instrument discussion: cost shifters, other-market airline fares (Hausman type), competitive flight frequency (Stern type), and nonprice characteristics. The chosen instruments are average JetBlue fares in other markets and Virgin America's nonstop flight frequency; validity requires relevance and exclusion restrictions, not merely a correlation with price.
- **Pages 8–10:** Econometric evidence. Authors report diagnostic tests of relevance and endogeneity. At the sample median price of **$199**, the OLS elasticity is approximately **-0.58** versus **-1.32** with 2SLS; at the mean price **$232**, approximately **-0.75** versus **-1.97**. The direction changes the implied fare decision. These are sample-specific estimates, not transferable coefficients.
- **Pages 11–12:** Heterogeneity. At the median price, elasticity varies across departure times, weekdays and booking horizon: roughly **-0.57** for 1–2 DFD versus **-1.89** for 22–28 DFD. Competitor promotions also influence response. The published estimates do *not* support one universal constant elasticity.
- **Pages 13–14:** Limitations and worked airline-promotion examples. Small market sample and many missing observations; unseen buyer characteristics; travel purpose and channel heterogeneity. Illustration of when fare discounts or competitor-price matching might improve modeled revenue explicitly omits capacity and subsequent competitor responses.
- **Pages 15–17:** Conclusions and bibliography. Position IV-derived flight-level price response as **input** to later joint pricing and inventory optimization, not a complete RM application.

### What we should adopt
Define a **price-response modeling interface** with inputs `flight context + candidate fare + observed competing offers` and an estimated booking response *plus uncertainty*. Record the fare **offered** each day, not just the fare paid by purchasers; retain booking date, departure date, and daily sales. When suitable data become available, compare naive OLS with price-endogeneity-aware estimators, and have a domain expert evaluate whether proposed IV assumptions are credible.

### What we should not claim
Do not train `demand = f(fare)` on monthly BTS DB1C purchases and call the slope a causal elasticity. Do not set the model's -1.2 scenario elasticity equal to Mumbower's actual finding: the coefficients depend on airline, market, flight, sample, and price level.

## Paper 2. Fan, Zhang & Lu (2026)
**Sales-target-oriented rule-based dynamic pricing system design for airlines.** International Journal of Engineering Business Management 18, 1–10. 10 PDF pages.

### All-page reading map
- **Pages 1–2:** Context and motivation for integrating real-time airline data, competitor prices, commercial targets and manager expertise with legacy reservations and distribution systems. Proposed system is **rule-based and target-driven** rather than an end-to-end deep learning predictor.
- **Page 3:** Defines pricing strategy around **RASK** (revenue / available-seat-km), **LF** (load factor) and **MDR** (minimum discount rate), with different priorities for monopoly, competitive and disadvantaged routes; uses data-collection points (DCPs) for reforecasting / repricing.
- **Page 4:** **Figure 1** connects sales/booking data, cleaning/unconstraining, forecast, bid prices and current inventory to target-driven rules and competitive signals. Historical similar-flight records can set regression targets; examples match weekday, season and market class. RASK modeled via a linear regression of operational/market features. Target LF and MDR percentile rules are policy choices, not universal optima.
- **Page 5:** **Figure 2** illustrates three-stage rule algorithm: update targets, calculate possible sales volumes and minimum discount, then use live sales and competitor levels to recommend a discount and allocation. Paper outputs include **recommended discount (LD)** and **seat quantity constraint (LAU)**; these are not exactly the same output as our recommended standalone net fare.
- **Pages 6–7:** Practical system design, **Figure 3**, with data processing, predictive analytics, decision analytics, results layers. EMSR/bid-price concepts underpin seat valuation. Integration with existing CRM/RMS/CRS is modular; human judgment remains important.
- **Page 8:** Operational engineering: indexed/partitioned data structures, staged scheduled computations, recompute stable parameters less often, keep real-time pricing fast. Its solutions target a large operational airline environment, not requirements we must copy prematurely.
- **Page 9:** Reported implementation outcomes include around **0.53% year-over-year observed revenue difference** (not by itself a randomized causal effect) and simulated advantages of **3.23% / 8.06% / 4.78%** against an EMSRb comparator on business / tourism / standard routes. Data from an airline in China are nonpublic, so replication is constrained.
- **Page 10:** References covering continuous pricing, leg controls, booking systems, and earlier forecasting approaches.

### What we should adopt
Use the **four-layer separation** as a blueprint: data ingestion / validation; analytics/forecast; optimization and rules; results and monitoring. Add **reforecast checkpoints**, human approval, and a route-specific policy configuration that can later represent LF/RASK/discount targets. Do not prematurely implement distributed storage and high-concurrency designs designed for an operating carrier.

### What we should not claim
Our current `±20%` price grid is **not** Fan's actual target-driven MDR/LAU algorithm. It is a simple decision-engine baseline inspired by the same class of problems. Revenue-gain percentages from a Chinese airline should not be used as Skytech projections.

## Paper 3. Belobaba (2016)
**Optimization models in RM systems: Optimality versus revenue gains.** Journal of Revenue and Pricing Management. 7 PDF pages.

### All-page reading map
- **Page 1:** Introduces the gap between theoretical optimality and actual realized revenue under violated assumptions.
- **Page 2:** Single-leg seat allocation: Littlewood rule, EMSR/EMSRb, optimal booking limits, dynamic programming (DP). Static, frequently updated heuristics can perform as well as or better than “optimal” models whose demand arrival assumptions are wrong.
- **Page 3:** Studies how demand variance changes performance. Explains that complex network control requires valuing a seat used by an itinerary that may traverse several legs; distinguishes network linear programming, DAVN and probabilistic bid-price controls.
- **Page 4:** Network DP complexity, fare adjustments and the risk of **buy-down** (people choosing cheaper available fares). A model may be mathematically optimal under unrealistic independent fare-class demand assumptions.
- **Page 5:** Comparison architectures: DAVN, PROBP, DAVN-UDP. **Figure 1** shows combinations of forecasts, LP/DP, virtual buckets, price adjustments and seat availability controls. Performance depends on recomputation frequency and forecast type.
- **Page 6:** **Figure 2** is a simulated comparison, not an empirical validation for every airline. Example gains relative to leg-based RM: DAVN **0.51%** with less frequent reoptimization, **0.76%** daily; PROBP **0.66%** daily; DAVN-UDP **1.10%**. Hybrid forecasting / fare adjustment further changes gains. Concludes that actual data assumptions and system configuration matter more than mathematical purity alone.
- **Page 7:** References to the underlying EMSR, DP, demand forecasting and network inventory control literature.

### What we should adopt
Maintain a **simple transparent baseline** and compare against each advanced alternative using the same synthetic or historical holdout scenario, demand assumptions and operational constraints. Continue single-leg flights for MVP, but future multiple fare classes may warrant EMSRb even without connecting flights. Define validation metrics for **decision performance** as well as forecasting accuracy.

### What we should not claim
Belobaba did not specifically endorse the isoelastic formula `Q(p)=Q0(p/p0)^epsilon` or our price grid; his article discusses **inventory allocation and optimization tradeoffs**, not a particular constant-elasticity fitting scheme.

## Paper 4. Wang, Wen, Lin, Pan, Wu & Zhuang (2025)
**Integrated demand forecasting and capacity control for segment-based airline revenue management.** International Journal of Engineering Business Management 17, 1–12. 12 PDF pages.

### All-page reading map
- **Pages 1–2:** Central problem: observed ticket sales are **censored** by closed fare classes and sold-out flights. Forecasting observed sales underestimates actual unconstrained interest; studying prediction separately from RM policy neglects feedback effects.
- **Page 3:** Data: one business-intensive Chinese airline route, eight daily flights, 2018–2019 history. Stop/capacity patterns available. Economy's 17 fare classes grouped into five virtual categories. Single-leg and economy-only scope; no network optimization.
- **Page 4:** Historical transaction and control data; exclusions and modeling assumptions (independent fare-class demand, often normal demand, limited treatment of cancellations and groups). **Figure 2** shows four evaluation modules: forecasting, capacity optimization, forecast evaluation and policy evaluation. *Important:* the paper does not solve our entire dynamic customer-facing fare-selection problem.
- **Page 5:** **Figure 3** depicts unobserved demand after a class closes or availability vanishes. **EM** estimates missing demand by conditional expectations and re-estimating distribution parameters. **PD** replaces part of this with quantile/median based estimation; the normal-demand assumption is material.
- **Page 6:** **Figure 4**: train/test split. Unconstrain historical training demand, then fit a **Lasso-regularized linear model** forecasting fare-class mean and residual variance. Gaussian mean/variance are outputs for subsequent capacity control; a point forecast alone is insufficient for classical EMSR.
- **Page 7:** Describes the seat protection optimization problem and **EMSR-a/EMSR-b** heuristic variants. Both use higher-fare demand distribution estimates to reserve inventory, not directly calculate a continuously published price.
- **Page 8:** **Figures 5–7** illustrate the seat-control flow, forecast evaluation, and control-policy evaluation. Forecasts are evaluated on Sep–Dec 2019 after training earlier in 2018–2019, with MAE and MAPE, then the seat-control strategies are compared in repeated Monte Carlo simulations.
- **Page 9:** Results: revenue MAE decreased from **28,758 CNY** (linear model without unconstraining) to **21,099 CNY** (LR+EM) and **20,079 CNY** (LR+PD). In this experiment PD performed best overall, most dramatically for heavily censored cheap classes. Do not universalize the ordering of PD and EM.
- **Page 10:** **Table 4**: simulated expected revenue of **105,337 CNY** for experience-based control, versus **133,311 CNY** with EMSR-a and **132,872 CNY** with EMSR-b, using the paper's enhanced forecasting setup (reported **26.6%** and **26.1%**). This is **scenario-specific simulation gain**, not a causal measured profit lift in Iran or at Skytech.
- **Page 11:** Conclusions and limitations: class independence, normality, selected route, no network interaction or price-competition response. Further work suggested on robust modeling, alternative uncertainty distributions, and richer data.
- **Page 12:** References on censoring, demand estimation, EMSR and single-leg capacity control.

### What we should adopt
Once Skytech has the corresponding raw logs, implement **observed-sales pickup baseline → unconstraining candidates (PD / EM) → Lasso-style forecast with mean and uncertainty → simple capacity control / EMSRb**. Use time-based, out-of-sample evaluation and decision simulation. Preserve raw booking dates, fare availability/closures and inventory history. A one-month BTS ticket sample cannot identify unseen demand.

### What we should not claim
Wang's ~26% improvement is not a prediction of achievable live revenue; it compares simulated policy choices in a specific airline case. EMSR-b is not always numerically superior even in its own study (EMSR-a slightly outperformed EMSR-b there).

## Comparative implementation matrix

| Workstream | Strongest anchor | Our current implementation | Next justified step | Missing data |
|---|---|---|---|---|
| Data + operations | Fan 2026 | BTS Parquet processing | Flight-level schema and validation | Booking/inventory histories |
| Historical demand unconstraining | Wang 2025 | Not implemented | Identify censored availability; PD/EM later | Fare closures, sold-out periods, sales history |
| Baseline forecast | Wang 2025 | 60 future bookings manually entered | Simple booking-pickup baseline; then Lasso | Timestamped flight bookings with DTD |
| Price response | Mumbower 2014 | Isoelastic assumption (e.g. -1.2) | Collect offer prices & test naive vs causal estimation | Offered fares, competitors, bookings and credible IV/exogenous variation |
| Capacity | Wang + Belobaba | Cap sales by remaining seats | Multiple fare-class protection / EMSRb as needed | Flight class mix, uncertainty, booking inventory |
| Decisions | Belobaba + Fan | Grid -20% to +20%, 5% step | Decision evaluation, guardrails and human approval | Rules, approvals, outcomes |
| Evaluation | Wang + Belobaba | Initial unit tests, basic sensitivity | Historical holdout, scenario stress tests, monitored pilot | Actual historical outcomes |

## Architecture: refine, do not rebuild

**TRAINING / RESEARCH PATH**
`Airline events + inventory/offer snapshots + market context -> validate/feature engineer -> detect censoring -> unconstrain where identifiable -> fit & evaluate demand forecast -> separately estimate conditional price effect (address endogeneity) -> store versioned, calibrated models.`

**INFERENCE / LIVE DECISION PATH**
`Flight at timestamp t + remaining seats + current/reference fare + route/season/competition + airline policy -> baseline future bookings + forecast uncertainty + conditional price response -> candidate-price revenue distribution / marginal capacity value -> optimize only feasible fares -> explain + approval -> publish externally if authorized -> observe outcomes -> monitoring/retraining.`

The current source code implements only a **scenario** along this second path. Uncertainty and lost-sales censored demand are not yet trained.

## Immediate research and engineering action plan

1. **Request a permissioned, de-identified pilot dataset from Skytech's airline advisors.** Choose one nonstop route and ideally 12+ months of history. Record historical flight ID, departure timestamp, per-day bookings, cancellation adjustments, historic fares *offered*, fare class and open/closed status, remaining capacity snapshots, and route/calendar context. Avoid passenger names, contact details, PNR secrets and unneeded identifiers. If only aggregated counts can be shared, begin with them.
2. **Write a data contract.** Explicit granularity: `one flight departure × one observation date` (and fare class if applicable). Prevent future leakage from the reporting date. Define whether fare includes taxes and fees.
3. **Baseline before sophistication.** Use similar-flight pickup averages, then regularized linear regression (Lasso/Ridge) with proper time holdout. Metrics: MAE, WAPE or another well-defined demand metric, interval coverage and business outcome. For censored classes, separately review whether these metrics are meaningful on observable sales.
4. **Unconstraining, only where possible.** Compare no correction to PD and EM against a transparent simulated censoring experiment and any observed high-availability cases.
5. **Price response, separately.** Maintain an assumed isoelastic curve in scenarios until credible offered-price/booking variation is available. Price endogeneity cannot be fixed by training a larger model alone. Review instrument assumptions, possible pilot price experiments, or other identification strategies with a qualified economist/OR collaborator.
6. **Decision simulation.** Replay/simulate bookings under fixed capacity, compare policies with a common scenario generator, quantify regret, worst-case revenue, spoilage and displacement; don't infer realized profit from offline counterfactual comparisons.
7. **Human-in-the-loop pilot.** Approval log, rollback of recommendations, policy limits, no autonomous fare publishing until explicitly authorized.

## Proposed Skytech × RIML academic scoping

**Roles:** Skytech owns the airline operational question, domain advisors, business guardrails, permissioned data access and product integration. RIML may contribute forecasting uncertainty, shift/robustness tests, model evaluation, and methodology review; airline RM/operations researchers should jointly advise capacity control and causal estimation.

**First proposal:** A **time-boxed 4–6 week feasibility study**, contingent on CEO approval and mutual agreement, rather than asking for open-ended lab co-ownership.

**Question:** Can conditional flight-level booking pickup and decision outcomes be predicted reliably under censored sales, price endogeneity, seasonal shift, and limited operational data? Which simple or advanced method is measurably better?

**Deliverables:** agreed data schema, non-sensitive or privacy-safe pilot data, transparent baselines, evaluation protocol, error/uncertainty report, recommendation on whether deeper R&D is justified.

**Governance to settle *before* exchanging nonpublic data or code:** Skytech permission to communicate externally; data rights, confidentiality/NDA, data retention and access, regulatory and cross-border handling, foreground/background IP, GitHub and publication permissions, student credit, scope, cost/resource allocation, milestone-based exit criteria, and the user's engineering responsibility/recognition. The proposal is **not** evidence that the lab has agreed to participate.

## Key distinctions to present honestly

- **Sampled sold fares are not a booking curve:** BTS June 2026 can benchmark historical fares, not reconstruct 60 expected future bookings on a named flight.
- **Forecast accuracy is not causal price effect:** a perfect `Q at today's prices` predictor can still price badly if it does not correctly model a price intervention.
- **Capacity cap is not EMSR:** `min(expected bookings, seats)` is a necessary feasibility rule, but not a model of the value of saving a seat for higher-paying future customers.
- **Robustness is not guaranteed by simplicity:** the sensitivity-analysis finding that multiple tested elasticities choose the +20% guardrail demonstrates dependence on the demand/capacity scenario and coarse grid. Simulate multiple demand levels, price curves and forecast errors before describing a decision as robust.
- **Revenue is not profit:** operating cost integration is a later workstream.
- **Historical/simulated research revenue improvements are not Skytech forecasts.**

## Citations

1. Mumbower, Stacey, Laurie A. Garrow, and Matthew J. Higgins. 2014. *Transportation Research Part A* 66:196–212. DOI: 10.1016/j.tra.2014.05.003.
2. Fan, Wei, Yingfeng Zhang, and Liang Lu. 2026. *International Journal of Engineering Business Management* 18:1–10. DOI: 10.1177/18479790261416546.
3. Belobaba, Peter P. 2016. *Journal of Revenue and Pricing Management*. DOI: 10.1057/rpm.2016.13.
4. Wang, Surui, et al. 2025. *International Journal of Engineering Business Management* 17:1–12. DOI: 10.1177/18479790251407499.


---

# Research update — Paper 5, Iran-specific uncertainty and crisis response (23 October 2026)

## Paper 5 — Almasi & Bagherian (2025)
**Airline pricing: an uncertain programming approach.** OPSEARCH, DOI: `10.1007/s12597-025-00998-8`. **28 PDF pages.** The paper uses Baoding Liu's **Uncertainty Theory**, which formalizes elicited *degrees of belief* rather than conventional empirical probabilities. It studies three cabin classes (economy, business, first) in an Iranian-agency example. This is a **specialized stress/ambiguity reference**, not a replacement for our four foundation papers.

### Complete-page reading map (PDF page numbers)
- **pp. 1–2:** Abstract, problem motivation and advertised contributions. Paper claims theory-based pricing is more useful when data is scarce or unstable; distinguishes beliefs from probability distributions. Its high-level revenue comparisons are numerical results, not verified generalizable operational gains.
- **pp. 3–7:** Extensive literature review and Table 1; covers stochastic, robust, fuzzy, choice, dynamic-pricing and inventory-control methods. Important gap: volatility and historical data inadequacy. Literature discussion is not a systematic empirical head-to-head evaluation of all named methods.
- **pp. 8–11:** Liu's uncertainty measure axioms and distribution/expected value definitions. They are formal mathematical assumptions, not calibrated real-world probabilities; expert beliefs need elicitation design and validation.
- **p. 12:** Figure 1 research process: define criteria → Delphi/expert consultation → derive uncertainty distributions → solve and run sensitivity analysis. Introduces 3-class notation.
- **pp. 13–15:** **Model 1 (Eqs. 18–25)** maximizes expected revenue from class-specific fulfilled-demand variables, under class seat limits and a price constraint modified by *inflation* (omega) and *seasonality* (delta). Important: fulfilled demand is not explicitly estimated as a function of candidate price within this formulation. A condition that all seats must sell appears in the description and strong/full-sale logic, but it is not an appropriate general airline policy when demand is low or a flight is cancelled.
- **pp. 15–16:** **Model 2 (Eqs. 26–28)** adds uncertain class demand and `min(M_j, D_j)` capacity-limited sales. This is conceptually closer to our current `min(expected demand, remaining seats)` calculation, **but still not a derived flight-level price-response function**. Neither model substitutes for Mumbower-style causal elasticity.
- **pp. 16–17:** Elicitation: Delphi-informed questionnaires and piecewise uncertainty distributions, then an Iranian airline-agency example. Paper gives a 360-seat configuration (260 economy, 90 business, 10 first), illustrates price ratios, inflation/seasonal factors and reported optimized fares. Treat these as *case-study assumptions*, not representative Iranian aircraft or regulations.
- **pp. 18–19:** Numeric worked problem and reported fare choices; three scenario types are introduced. Critically, check the published equations/ratios before attempting to reproduce the values: the stated first/business ratio and reported price ratios do not fully align, and the displayed price bound constraints do not by themselves uniquely explain all reported fares. This is a reproduction question, not proof of a computational error.
- **pp. 20–23:** Tables 2–4 and Figures 2–4 compare Model 1, Model 2, stochastic and robust alternatives in **three constructed scenarios**: (1) high-demand/low price sensitivity, (2) moderate demand/high price sensitivity and (3) low demand/economic instability. Example first-scenario revenues: Model 1 **$12,741.82**, Model 2 **$10,064.19**, stochastic **$11,126.43**, robust **$8,990.83**. These are *within-scenario simulated outputs* and depend on selected constraints, fares and assumptions; their differences are not proven advantages under real war shocks.
- **pp. 24–25:** Conclusion and explicit limitations: subjective belief bias, reproducibility, fixed configuration/single-leg restrictions and growing computation with more uncertain inputs; recommends hybrid approaches and adaptive learning.
- **pp. 25–28:** References and rights. Relevant leads include McAfee & te Velde (2008) on constant demand elasticity, Feng et al. on partial-information robust pricing, and Gallego & Topaloglu on pricing analytics. Any reuse of tables/figures must respect publisher rights.

### The useful method in plain English
1. In a crisis, normal historical relationships between fare, bookings and seasonal effects may break down.
2. Ask multiple experienced airline managers for **ranges and confidence judgments**, *not just a guessed single number*.
3. Record the information source, confidence and timestamp and derive explicit **scenario distributions** or belief curves.
4. Run the *same feasible pricing candidates* through baseline, risk-aware and expert-informed models; compare business outcomes.
5. Apply hard constraints (fare policies, remaining physical seats, flight-operational status) and require human sign-off when the model is outside its tested domain.
6. Measure forecast reliability and outcome over subsequent flights, recalibrate or remove expert overrides based on evidence.

### Critical scientific caveats
- **Belief degree is not a frequentist probability.** Do not interpret expert inputs as objectively estimated event frequencies.
- **No automatic causal elasticity:** price-dependent booking response cannot be identified from expert inflation/seasonality factors alone.
- **Objective limitations:** Model 1 can favor boundary fares when assumed sales do not react to fare; adopting it alone could overprice or underfill flights.
- **Benchmarking fairness:** The scenario comparison is not a randomized controlled test, nor a shared independently calibrated backtest with airline realized earnings. The paper does not justify claiming that stochastic or robust methods universally fail during war.
- **Numerical reproducibility:** Follow up on the worked 360-seat, class ratios and displayed price-bound calculations before making a software replica. Preserve a source-exact version of the assumptions; don't quietly fix them and cite the paper as if unchanged.
- **Context:** 'Iranian airline agency' in the worked example is not proof the proposed optimizer has been deployed or measured across an airline network.

### Specific Iran-relevant failure modes and our possible remedies (engineering proposals, not verified current events)

| Scenario / shock | Risk to our model | Proposed observable signal / input | Safe response |
|---|---|---|---|
| Geopolitical/airspace restrictions | Sudden cancellations, route suspension, infeasible flight | Flight-operation status and approved schedule; NOT price data alone | **No pricing recommendation** if cancelled/suspended; block publication |
| Temporary capacity/fleet disruption | Aircraft substitution, scarce aircraft/spares, capacity change | Updated operating capacity, aircraft assignment, sales restrictions | Re-run feasible optimization and log inventory change |
| Inflation / exchange-rate shift | Nominal fares incomparable over time, cost-floor mismatch | Currency, timestamped FX basis, inflation index where lawful and relevant | Normalize historical prices and keep business/legal fare constraints separate |
| Demand regime change during unrest | Pre-crisis pickup curve no longer predicts | Change-point / drift indicators, recent bookings, route-specific cancellations | Warn as **out of distribution**; shorten lookback, widen scenario ranges, manual review |
| Fuel / maintenance / airport disruption | Schedule and cost shock; normal sales no longer sufficient | Operational advisories and authoritative airline status | Gate decisions on operating feasibility; later combine with cost model |
| Poor/incomplete airline data | Hidden censored demand, missing fares, late updates | Data freshness, missingness, availability snapshots | Disable auto decision, retain transparent manual scenario mode |
| Holiday surge, e.g. Nowruz | Time-varying preference and seat scarcity | Calendar, departure date, comparable flights | Use season-specific forecast and policy; do not transplant paper coefficients |

### Recommended scenario architecture (future layer)
Create a **Risk / Regime Context** service alongside normal flight context, not a replacement forecast. Its outputs should be `operational_status`, `regime_label`, `data_freshness`, `source_of_truth`, `expert_adjustment`, `uncertainty_range`, `confidence_flag`, `policy_version`. This feeds a **scenario evaluator** and a **no-recommendation / manual-review gate**. The regular demand forecast and price-response modules remain separately versioned. Price caps and published-fare/tax basis must be validated against actual route/date regulatory and airline policy data, never guessed.

### Test plan before adopting Uncertainty Theory
- **Baseline A:** historical pickup or Lasso demand forecast + simple price-response assumptions + existing grid search.
- **Alternative B:** baseline with **risk scenarios** (low/base/high demand, elasticity alternatives, capacity shocks), *same price candidates and constraints*.
- **Alternative C:** expert-elicited belief-based version of Almasi/Bagherian's model, accurately reproduced *after* clarifying its published numeric assumptions.
- **Alternative D:** conservative scenario/robust optimization baseline with user-approved loss/risk criterion.
- **Comparison:** simulated/observed remaining-seat revenue where defensible, regret across shocks, seats unsold, violations, failure-to-recommend rate, forecast error/calibration, time to compute, and reliance on subjective assumptions.
- **No information leakage:** All features and expert inputs must be available at the **decision timestamp**, not learned after departure.

**Decision:** add uncertainty-aware scenario analysis and an operational fallback **after** establishing the flight-level data contract. Keep the simple current pricing engine unchanged for now; the new paper is a research alternative to evaluate, not a production algorithm to install today.

## Interpreting Fan's +0.53% correctly

Fan (2026), PDF p. 9, contrasts average flight revenue after deployment against **the same period in the prior year, when an EMSR-based and heavily manual/static RM system existed**. Thus it is neither a no-RM control group nor a randomized same-season A/B test. A 0.53% relative revenue difference may be commercially significant at scale, but market/year differences confound causal attribution. It cannot be compared directly with Wang's ~26% simulated gain or the 3.23/8.06/4.78% simulations in Fan. We should establish the baseline (existing Skytech/partner RM policy), metrics, experiment design and operating conditions before projecting uplift.

## Review of uploaded interactive architecture (HTML, 23 October 2026)

**Assessment:** strong two-pipeline concept, comprehensible clickable detailed/minimal display, separated forecasting and elasticity, explicit approval, validation and feedback. **Keep the structure**, amend technical/operational labels below.

| Current diagram issue | Corrected description |
|---|---|
| Formula `max E[D(P; mu,sigma,epsilon) * (P - pi)]` | Current MVP objective is **expected remaining-seat revenue** `max_P P * E[min(D(P), S_remaining)]` under feasibility. If `pi` is a future-seat opportunity cost, define it rigorously and **avoid double-counting** capacity value. Do not display a speculative joint objective as implemented. |
| Forecast states `mu, sigma` but calls sigma `variance` and fare 'confidence interval' | `mu` = mean, `sigma` = standard deviation, `sigma^2` = variance. A predictive interval or an uncertainty range requires additional calibration; **sigma itself is not a confidence interval**. |
| `Causal elasticity via IV` shown as universal | Change to 'Price-response estimation; causal IV/experiment only if identifiable and validated'. An instrument is not valid by default; constant-elasticity remains the unvalidated current assumption. |
| `P(Buy|P)`, `elasticity`, WTP shown interchangeably | These are different possible parameterizations. Use one documented price-response API and indicate which model actually provides the outputs. |
| Production-sounding 'Live', 'Real-Time', 'vX.Y ready', 'Auto-Approve', 'Push to GDS/PSS' | Clearly separate **implemented MVP (manual/simulated, recommendation only)** from **future integrations**. No automatic price publishing or approval in today's MVP. |
| `EM / Projection` always appears in data preparation | Say `censoring detection -> PD/EM unconstraining if data supports it`; BTS DB1C cannot reconstruct flight-level censoring. |
| Blanket 'outlier filtering' | Specify documented domain quality rules; retain genuine extreme fares unless justified, segregate tax-only / invalid rows. |
| No crisis-specific operational gate | Add `Risk / Regime Context` and an **availability + freshness + legal validity check**; cancellation/suspension => no recommendation. |
| Capacity model `EMSR / shadow price` | Show as **optional, data-dependent future component**; current single-leg one-fare scenario only caps sales with seats. |
| In-solver fare bounds plus post-optimizer check | Good: enforce hard feasibility **within** optimizer, check again before human recommendation. Keep user's existing experimental **+/-20%, 5% grid**; do not represent it as legal or universal. |

**UI/UX amendments for Gemini:** label **Current MVP / Target Architecture**, add plain-language glossary and source citations in expandable details, make 2-column vs stacked readable on laptop/mobile, preserve keyboard-accessible interactions, use status text not only color, provide print/export view, reduce noisy badges, and include source/provenance and model confidence status. If the HTML should work without Internet, do not rely on Tailwind and Google Fonts CDNs alone.

## Canonical repository documentation policy

Keep **exactly three maintained Markdown documents**:

1. `/README.md`: project elevator pitch, architecture summary, current capabilities/limitations, repo structure, setup/run/test/demo, navigation and quick handoff.
2. `/docs/research_and_findings.md`: **this document**, canonical paper-by-paper review, assumptions, architecture/method decisions, data needs, experiment comparisons and citations.
3. `/docs/devlog.md`: chronological verified steps and commands, test results, Git milestones, outstanding tasks and next-step checkpoint; append, don't overwrite history.

Store the interactive architecture as a **non-Markdown supporting asset** at `/docs/architecture/airline_rm_architecture.html`; it must not become a second source of truth for implementation status. Prefer Git-tracked small code/docs and retain raw downloadable Parquet outside Git. Do not duplicate this research document under multiple filenames in the repository.

### Handoff snapshot
- Stack: Windows 11 → WSL2 Ubuntu 24.04 → Python 3.12 `.venv` → DuckDB/Pandas → Streamlit; GitHub `origin/main` (last known push includes pricing dashboard/tests).
- Public data: BTS DB1C June 2026, Ticket **13,822,006** sampled rows/39 fields; Market **57 fields**; selected AA ORD→LGA nonstop, **14,035 rows**, ex-tax median `$169.76` in `data/processed/aa_ord_lga_nonstop.parquet`.
- MVP models: `src/demand.py` isoelastic assumed epsilon, `src/optimizer.py` price grid **+/-20%** in 5% steps and `min(demand, seats)` capacity; `app.py` Streamlit; `src/sensitivity_analysis.py` demonstration.
- User-provided experiment: with reference price $170, baseline future demand 60, remaining 45 seats, epsilon -0.6/-1.0/-1.2/-1.5 all choose **$204**, epsilon -2.0 chooses **$195.50**. These are **scenario results**, not calibrated model performance.
- No verified live flight bookings, price-offer history, censoring logs, causal price-response model, trained demand predictor, regulatory-price integration, cost model or live airline publishing.
- **Next engineering checkpoint:** scope/anonymize one-route historical airline booking and inventory dataset and write a clear per-flight/per-day data contract; run current dashboard/tests locally; then compare historical pickup average vs Lasso baseline with chronological holdout. Paper-inspired EM/PD/IV/EMSR and crisis methods are **candidates** to evaluate only when proper data arrive.
