# Efficiently Tracking GOO Total Virtual Supply - Maths
## Definitions
- $m_i$  total goo emissions multiple (`getUserData[i].emissionMultiple`)
- $b_i$  last user balance (`getUserData[i].lastBalance`)
- $m_{g,i}$  emissions multiple of gobbler $i$ (`getGobblerData[i].emissionMultiple`)
- $t_{0,i}$ time of last balance update for account $i$
## New Definitions
- $\Delta t$ time since last global trackers were updated
- $t_0$ time of last global update
## Individual GOO Production
$g(m_i, b_i, \Delta t_i) = b_i + \frac{1}{4}\cdot m_i\cdot\Delta t^2 + \Delta t\cdot\sqrt{m_i \cdot b_i}$ 
## Total Supply
Total supply $T$ after $\Delta t$ since last update $T' = \sum_{i=0}^n g(m_i,b_i,\Delta t)$

Assuming the total supply accumulators are always updated on every transfer or emissions multiple change (reveal, legendary gobbler mint) $\Delta t$ is the time passed since the last update and therefore identical for all accounts:

$$ T' = \sum_{i=0}^n  (b_i + \frac{1}{4}\cdot m_i\cdot\Delta t^2 + \Delta t\cdot\sqrt{m_i \cdot b_i}) $$
$$ T' = \sum_{i=0}^n  b_i + \sum_{i=0}^n (\frac{1}{4}\cdot m_i\cdot\Delta t^2 )+\sum_{i=0}^n (\Delta t\cdot\sqrt{m_i \cdot b_i}) $$
$$ T' = \sum_{i=0}^n  b_i + \frac{1}{4}\cdot \Delta t^2\cdot\sum_{i=0}^n m_i +\Delta t\cdot\sum_{i=0}^n \sqrt{m_i \cdot b_i} $$
$$ T' = T + \frac{1}{4}\cdot \Delta t^2\cdot M +\Delta t\cdot Z$$

## Updating $M$, $Z$
$b_x' = g(m_x, b_x, \Delta t_x)$
### Transfers
Transfer of gobbler $a$ from account $i$ to $j$:
- $T' = T + \frac{1}{4}\cdot \Delta t^2\cdot M +\Delta t\cdot Z$
- $m_i' = m_i - m_{g,a}$
- $m_j' = m_j + m_{g,a}$
- $M' = M$
- $\hat b_x = g(m_x, b_x, t_0 - t_{0,x})$
- $Z' = Z  + \frac{1}{2}\Delta t\cdot (M - m_i - m_j)+ (\sqrt{m_i' \cdot b_i'} - \sqrt{m_i \cdot \hat b_i}) + (\sqrt{m_j' \cdot b_j'} - \sqrt{m_j \cdot \hat b_j})$

### Emissions Multiple Change (Reveal / Legendary Gobbler Mint)
Reveal / Legendary gobbler mint resulting in emissions multiple change $\Delta m$ for account $i$:
- $T' = T + \frac{1}{4}\cdot \Delta t^2\cdot M +\Delta t\cdot Z$
- $M' = M + \Delta m$
- $m_i' = m_i + \Delta m$
- $\hat b_i = g(m_i, b_i, t_0 - t_{0,i})$
- $Z' = Z + \frac{1}{2}\Delta t\cdot (M - m_i) + (\sqrt{m_i' \cdot b_i'} - \sqrt{m_i \cdot\hat b_i})$

### Virtual GOO add / remove
Change in the virtual goo balance $\Delta b$ of account $i$:
- $T' = T + \frac{1}{4}\cdot \Delta t^2\cdot M +\Delta t\cdot Z + \Delta b$
- $M' = M$
- $\hat b_i = g(m_i, b_i, t_0 - t_{0,i})$
- $b_i' = g(m_i, b_i, \Delta t_i) + \Delta b$
- $Z' = Z + \frac{1}{2}\Delta t\cdot (M - m_i) + \sqrt{m_i}\cdot(\sqrt{b_i'}-\sqrt{\hat b_i })$
The intermediate previous balance $\hat b_i$ is required to ensure that $\Delta t = \Delta t_{\hat i}$


### Derivation of $Z$ Update
The following is the derivation of the $Z$ update for a transfer. The proof for updating $Z$ after an emissions multiple change is nearly identical excpet that only $i$ is excluded from the sum and split out.
$$Z' = \sum_{x=0}^n \sqrt{m_x'\cdot b_x'}$$
$$Z' = \sum_{x=0,x\ne i,j}^n \sqrt{m_x\cdot b_x'} + \sqrt{m_i'\cdot b_i'}+ \sqrt{m_j'\cdot b_j'}$$
$$Z' = \sum_{x=0,x\ne i,j}^n (\sqrt{m_x\cdot g(m_x,b_x,\Delta t)}) + \sqrt{m_i'\cdot b_i'}+ \sqrt{m_j'\cdot b_j'}$$
$$Z' = \sum_{x=0,x\ne i,j}^n (\sqrt{m_x\cdot (b_x + \frac{1}{4}\cdot\Delta t^2\cdot m_x+\Delta t\cdot\sqrt{m_x\cdot b_x})}) + \sqrt{m_i'\cdot b_i'}+ \sqrt{m_j'\cdot b_j'}$$
$$Z' = \sum_{x=0,x\ne i,j}^n \sqrt{m_x\cdot(\sqrt{b_x}^2 + 2\cdot \sqrt{b_x}\cdot\frac{1}{2}\cdot\sqrt{m_x}\cdot\Delta t + (\frac{1}{2}\cdot\sqrt{m_x}\cdot\Delta t)^2  )  } + \sqrt{m_i'\cdot b_i'} + \sqrt{m_j'\cdot b_j'}$$
$$Z' = \sum_{x=0,x\ne i,j}^n \sqrt{m_x\cdot(\sqrt{b_x} + \frac{1}{2}\cdot\sqrt{m_x}\cdot\Delta t  )^2  } + \sqrt{m_i'\cdot b_i'} + \sqrt{m_j'\cdot b_j'}$$
$$Z' = \sum_{x=0,x\ne i,j}^n (\sqrt{m_x}\cdot(\sqrt{b_x} + \frac{1}{2}\cdot\sqrt{m_x}\cdot\Delta t))   + \sqrt{m_i'\cdot b_i'} + \sqrt{m_j'\cdot b_j'}$$
$$Z' = \sum_{x=0,x\ne i,j}^n \sqrt{m_x\cdot b_x} +\sum_{x=0,x\ne i,j}^n (\frac{1}{2}\cdot\Delta t\cdot m_x) + \sqrt{m_i'\cdot b_i'} + \sqrt{m_j'\cdot b_j'}$$
$$Z' = \sum_{x=0,x\ne i,j}^n \sqrt{m_x\cdot b_x} +\frac{1}{2}\cdot\Delta t\cdot \sum_{x=0,x\ne i,j}^n m_x + \sqrt{m_i'\cdot b_i'} + \sqrt{m_j'\cdot b_j'}$$
$$Z' = (Z - \sqrt{m_i\cdot b_i}- \sqrt{m_j\cdot b_j}) + (\frac{1}{2}\cdot\Delta t\cdot(M - m_i - m_j)) + \sqrt{m_i'\cdot b_i'} + \sqrt{m_j'\cdot b_j'}$$
$$Z' = Z  + \frac{1}{2}\Delta t\cdot (M - m_i - m_j)+ (\sqrt{m_i' \cdot b_i'} - \sqrt{m_i \cdot b_i}) + (\sqrt{m_j' \cdot b_j'} - \sqrt{m_j \cdot b_j})$$
## Proof Of $T$ Update Consistency
Assuming no transfers, emissions or GOO balance changes, the following proves that updating $T$ after $\Delta t_1$ and $\Delta t_2$ is equivalent to updating once after $\Delta t_1  + \Delta t_2$:
$$T' = T_0 + \frac{1}{4}\cdot M\cdot(\Delta t_1 + \Delta t_2)^2 + (\Delta t_1 + \Delta t_2)\cdot Z_0 $$
$$T_1 = T_0 + \frac{1}{4}\cdot M\cdot\Delta t_1^2 + \Delta t_1 \cdot Z_0 $$
$$T_2 = T_1 + \frac{1}{4}\cdot M\cdot\Delta t_2^2 + \Delta t_2 \cdot (Z_0 + \frac{1}{2}\cdot M \cdot \Delta t_1) $$
$$T_2 = T_0 + \frac{1}{4}\cdot M\cdot\Delta t_1^2 + \Delta t_1 \cdot Z_0  + \frac{1}{4}\cdot M\cdot\Delta t_2^2 + \Delta t_2 \cdot (Z_0 + \frac{1}{2}\cdot M \cdot \Delta t_1) $$
$$T_2 = T_0 + \frac{1}{4}\cdot M\cdot\Delta t_1^2 + \Delta t_1 \cdot Z_0  + \frac{1}{4}\cdot M\cdot\Delta t_2^2 + \Delta t_2 \cdot Z_0 + \Delta t_2 \cdot \frac{1}{2}\cdot M \cdot \Delta t_1 $$
$$T_2 = T_0 + \frac{1}{4}\cdot M\cdot\Delta t_1^2 +  \Delta t_2 \cdot \frac{1}{2}\cdot M \cdot \Delta t_1 + \frac{1}{4}\cdot M\cdot\Delta t_2^2 + \Delta t_1 \cdot Z_0 + \Delta t_2 \cdot Z_0 $$
$$T_2 = T_0 + \frac{1}{4}\cdot M\cdot\Delta t_1^2 +  \Delta t_2 \cdot \frac{1}{2}\cdot M \cdot \Delta t_1 + \frac{1}{4}\cdot M\cdot\Delta t_2^2 + (\Delta t_1 + \Delta t_2) \cdot Z_0 $$
$$T_2 = T_0 + \frac{1}{4}\cdot M\cdot(\Delta t_1^2 +  2\cdot\Delta t_2 \cdot \Delta t_1 + \Delta t_2^2) + (\Delta t_1 + \Delta t_2) \cdot Z_0 $$
$$T_2 = T_0 + \frac{1}{4}\cdot M\cdot(\Delta t_1 + \Delta t_2)^2 + (\Delta t_1 + \Delta t_2) \cdot Z_0 $$
$$T_2 = T'$$
