from math import sqrt
from random import random, randint, seed


def goo_bal(m, b, t):
    return b + m * t**2 / 4 + t * sqrt(m * b)


def get_dual_sub_probs(main_prob, prob_a=0.5):
    return main_prob * prob_a, main_prob * (1 - prob_a)


def rand_emissions():
    if random() < 0.95:
        return randint(6, 9)
    return round(randint(25, 45) * 7.5)


class Account:
    def __init__(self, last_t, total_emis, last_bal):
        self.last_timestamp = last_t
        self.total_emissions = total_emis
        self.last_balance = last_bal

    @classmethod
    def gen_rand(cls, last_t):
        start_bal = random()**2 * 1000
        start_emis = sum(rand_emissions() for _ in range(randint(1, 8)))
        return cls(last_t, start_emis, start_bal)

    def update(self, t):
        self.last_balance = self.get_goo_bal_at(t)
        self.last_timestamp = t
        return self.last_balance

    def get_goo_bal_at(self, t):
        return goo_bal(self.total_emissions, self.last_balance, t - self.last_timestamp)

    def get_rand_goo_increase(self, t):
        # random multiplier between 0 and infinity
        x = 1 / (1 - random()**3) - 1
        return self.get_goo_bal_at(t) * x

    def get_rand_goo_decrease(self, t):
        # random multiplier between 0 and 1
        x = random()**5
        return self.get_goo_bal_at(t) * x

    def __repr__(self):
        return f'Account({self.last_timestamp:.2f}, {self.total_emissions}, {self.last_balance:.1f})'


def run_simulation(iters, time_per_iter, add_acc_prob, goo_probs, add_emis_prob,
                   transfer_prob, log_every=1000):
    # expand params
    add_goo_prob, sub_goo_prob = goo_probs

    # simulation state
    accounts = dict()  # id => Account
    last_acc_id = 0
    time = 0

    # total virtual goo supply tracking state
    last_total_supply = 0  # T
    total_emis = 0  # M
    last_Z = 0  # Z
    last_update = time  # t (such that Δt = t' - t)

    # simulation step output
    times = []
    real_total_goo = []
    calc_total_goo = []

    for i in range(iters):
        if log_every is not None and i != 0 and i % log_every == 0:
            print('i:', i)

        # save data at start of simulation step
        # # time
        times.append(time)
        # # real total goo
        total_goo = 0
        for acc in accounts.values():
            total_goo += acc.get_goo_bal_at(time)
        real_total_goo.append(total_goo)
        # # calculated total goo
        delta_t = time - last_update
        calc_total_goo.append(
            last_total_supply + 1/4 * delta_t ** 2 * total_emis
            + delta_t * last_Z
        )

        # run sim step
        r = random()

        if (r := r - add_acc_prob) <= 0:
            new_acc = Account.gen_rand(time)
            accounts[(last_acc_id := last_acc_id + 1)] = new_acc

            # update supply tracking
            last_total_supply += 1/4 * delta_t**2 * total_emis\
                + delta_t * last_Z\
                + new_acc.last_balance
            last_Z += 1/2 * delta_t * total_emis + \
                sqrt(new_acc.total_emissions * new_acc.last_balance)
            total_emis += new_acc.total_emissions
            last_update = time
        elif last_acc_id != 0:
            if (r := r - add_goo_prob) <= 0:
                acc = accounts[randint(1, last_acc_id)]
                goo_to_add = acc.get_rand_goo_increase(time)

                # update supply tracking
                last_total_supply += 1/4 * delta_t**2 * total_emis\
                    + delta_t * last_Z\
                    + goo_to_add
                last_Z +=\
                    1/2 * delta_t * (total_emis - acc.total_emissions) +\
                    sqrt(acc.total_emissions) * (
                        sqrt(acc.get_goo_bal_at(time) + goo_to_add) -
                        sqrt(acc.get_goo_bal_at(last_update))
                    )
                last_update = time

                # update account
                acc.update(time)
                acc.last_balance += goo_to_add
            elif (r := r - sub_goo_prob) <= 0:
                acc = accounts[randint(1, last_acc_id)]
                goo_to_sub = acc.get_rand_goo_decrease(time)

                # update supply tracking
                last_total_supply += 1/4 * delta_t**2 * total_emis\
                    + delta_t * last_Z\
                    - goo_to_sub
                last_Z +=\
                    1/2 * delta_t * (total_emis - acc.total_emissions) +\
                    sqrt(acc.total_emissions) * (
                        sqrt(acc.get_goo_bal_at(time) - goo_to_sub) -
                        sqrt(acc.get_goo_bal_at(last_update))
                    )
                last_update = time

                # update account
                acc.update(time)
                acc.last_balance -= goo_to_sub
            elif (r := r - add_emis_prob) <= 0:
                acc = accounts[randint(1, last_acc_id)]
                emis_to_add = rand_emissions()

                # update supply tracking
                last_total_supply += 1/4 * delta_t ** 2 * total_emis\
                    + delta_t * last_Z
                last_Z +=\
                    1/2 * delta_t * (total_emis - acc.total_emissions)\
                    + sqrt((acc.total_emissions + emis_to_add) * acc.get_goo_bal_at(time))\
                    - sqrt(
                        acc.total_emissions * acc.get_goo_bal_at(last_update)
                    )
                total_emis += emis_to_add
                last_update = time

                # update account
                acc.update(time)
                acc.total_emissions += emis_to_add
            elif len(accounts) >= 2:
                if (r := r - transfer_prob) <= 0:
                    # account selection
                    from_acc_id = randint(1, last_acc_id)
                    from_acc = accounts[from_acc_id]
                    to_acc_id = randint(1, last_acc_id-1)
                    if to_acc_id >= from_acc_id:
                        to_acc_id += 1
                    to_acc = accounts[to_acc_id]

                    emis_send = min(from_acc.total_emissions, rand_emissions())

                    # update supply tracking
                    last_total_supply += 1/4 * delta_t ** 2 * total_emis\
                        + delta_t * last_Z
                    last_Z +=\
                        1/2 * delta_t * (
                            total_emis - from_acc.total_emissions - to_acc.total_emissions
                        )\
                        + sqrt(
                            (from_acc.total_emissions - emis_send) *
                            from_acc.get_goo_bal_at(time)
                        )\
                        - sqrt(
                            from_acc.total_emissions *
                            from_acc.get_goo_bal_at(last_update)
                        )\
                        + sqrt(
                            (to_acc.total_emissions + emis_send) *
                            to_acc.get_goo_bal_at(time)
                        )\
                        - sqrt(
                            to_acc.total_emissions *
                            to_acc.get_goo_bal_at(last_update)
                        )
                    last_update = time

                    # update accounts
                    from_acc.update(time)
                    from_acc.total_emissions -= emis_send
                    to_acc.update(time)
                    to_acc.total_emissions += emis_send

        time += time_per_iter

    return real_total_goo, calc_total_goo, times
