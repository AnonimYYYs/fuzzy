import math


def E(m, v):
    return m * v * v / 2


def V(e, m):
    return math.sqrt(2 * e / m) if e > 0 else 0.0


# возвращает терм "высокая" скорость
def fuzzy_velocity(v):
    v_high = 50
    v_low = 10
    return 1.0 if v >= v_high else 0.0 if v <= v_low else (v - v_low) / (v_high - v_low)


# возвращает терм "близко"
def fuzzy_length(l):
    l_high = 100
    l_low = 50
    return 0.0 if l >= l_high else 1.0 if l <= l_low else (l - l_high) / (l_low - l_high)


def fuzzy_controller(v, l):
    fuzz_v = fuzzy_velocity(v)
    fuzz_l = fuzzy_length(l)
    return max(fuzz_l, fuzz_v)


def defuzzy(fuzzy_val, max_eng):
    return fuzzy_val * max_eng


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # variables
    mass = 1500.0                   # масса машины, кг
    velocity = 50.0                 # начальная скорость, м/с
    length = 500.0                  # начальное расстояние, м
    step = 1                        # сколько секунд длится один шаг моделирования
    energy_stop_max = 600000.0      # максимальная энергия торможения в секунду

    t = 0.0
    energy_stop_max *= step

    while True:
        curr_energy = E(mass, velocity)
        stop_energy = defuzzy(fuzzy_controller(velocity, length), energy_stop_max)
        new_energy = curr_energy - stop_energy
        new_velocity = V(new_energy, mass)
        print(f'time: {t},\t energy: {curr_energy},\t velocity: {V(curr_energy, mass)},\t stop energy: {stop_energy},\t lenght: {length}')
        length -= (velocity + new_velocity) * step / 2
        velocity = new_velocity

        if length <= 0:
            print(f'car broke; v={velocity}')
            break

        if velocity <= 0:
            print(f'car stopped; l={length}')
            break

        t += step
