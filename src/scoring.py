import numpy as np

#scoring logic for size, distance and velocity

def calculate_size_score(diameter_min_km, diameter_max_km):
    #transforms features into log mean
    diameter_mean_km = (diameter_min_km +diameter_max_km) / 2
    log_diameter_mean_km = np.log(diameter_mean_km)

    mean = log_diameter_mean_km.mean()
    sd = log_diameter_mean_km.std()
    #applies sigmoid function to generate value between 0 and 1
    z = (log_diameter_mean_km - mean) / sd

    size_score = 1 / (1 + np.exp(-z))
    return size_score

def calculate_velocity_score(relative_velocity_km_s):
    #upper limit of the historical dataset
    REF_VELOCITY = 60
    #quadratic scoring
    velocity_score = (relative_velocity_km_s / REF_VELOCITY) ** 2
    velocity_score = np.minimum(velocity_score, 1)
    return velocity_score

def calculate_distance_score(miss_distance_au):
    #NASA maximum miss distance to be classified as near-Earth object is 0.5 AU
    MAX_MISS_DISTANCE = 0.5
    distance_score = 1 - (miss_distance_au / MAX_MISS_DISTANCE)
    return distance_score

def calculate_risk_score(size_score, velocity_score, distance_score):
    #weights are informed by NASA and data analysis
    size_weight = 0.4
    velocity_weight = 0.3
    distance_weight = 0.3
    #risk score is the weighted sum of the risk component scores
    risk_score = (size_score * size_weight) + (velocity_score * velocity_weight) + (distance_score * distance_weight)
    return risk_score




