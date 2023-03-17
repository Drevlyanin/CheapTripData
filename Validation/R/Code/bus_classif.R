library(tidyverse)
library(readxl)
library(caret)
library(writexl)

#===============================================================================
# MODELING
#===============================================================================
# Data merge
bus <- read_excel("/Users/miss_viktoriia/Documents/CheapTrip/bus_for_labeling.xlsx") %>%
  select(from_id,
         to_id,
         price_min_EUR,
         duration_min,
         distance_km,
         frequency_tpw,
         Outcome) %>%
  filter(!is.na(Outcome))
countries <- read_excel("/Users/miss_viktoriia/Documents/CheapTrip/Full_list_with_countries.xlsx", 
                        range = "A1:H775", 
                        col_names = FALSE) %>%
  rename(id_city = ...1, 
         city = ...2, 
         id_country = ...3, 
         country = ...8,
         latitude = ...4,
         longitude = ...5) %>%
  select(id_city, 
         city, 
         id_country, 
         country, 
         latitude, 
         longitude)
locations_from <- countries %>%
  rename(from_id = id_city, from_city = city,
         from_country_id = id_country, from_country = country,
         from_latitude = latitude, from_longitude = longitude)
locations_to <- countries %>%
  rename(to_id = id_city, to_city = city,
         to_country_id = id_country, to_country = country,
         to_latitude = latitude, to_longitude = longitude)
connection_from <- left_join(bus, locations_from, by = c("from_id" = "from_id"))
connection_to <- left_join(connection_from, locations_to, by = c("to_id" = "to_id"))
bus_for_modeling <- connection_to %>%
  select(price_min_EUR,
         duration_min,
         distance_km,
         frequency_tpw,
         from_latitude,
         from_longitude,
         to_latitude,
         to_longitude,
         Outcome)
bus_for_modeling$Outcome <- as.factor(bus_for_modeling$Outcome)
# Feature engineering and scaling
scale_lat_from <- preProcess(bus_for_modeling[,5], method = "range",
                             rangeBounds = c(0.61, 1.01))
bus_for_modeling[,5] <- predict(scale_lat_from, newdata = bus_for_modeling[,5])
scale_lat_to <- preProcess(bus_for_modeling[,7], method = "range",
                           rangeBounds = c(0.61, 1.09))
bus_for_modeling[,7] <- predict(scale_lat_to, newdata = bus_for_modeling[,7])
scale_long_from <- preProcess(bus_for_modeling[,6], method = "range",
                              rangeBounds = c(-0.15, 0.48))
bus_for_modeling[,6] <- predict(scale_long_from, newdata = bus_for_modeling[,6])
scale_long_to <- preProcess(bus_for_modeling[,8], method = "range",
                            rangeBounds = c(-0.15, 0.46))
bus_for_modeling[,8] <- predict(scale_long_to, newdata = bus_for_modeling[,8])
set.seed(333)
ind <- createDataPartition(bus_for_modeling$Outcome, p = .8, list = FALSE)
train <- bus_for_modeling[ ind,]
test  <- bus_for_modeling[-ind,]

train <- train %>%
  mutate(log_price = log(price_min_EUR),
         log_duration = log(duration_min),
         log_dist = log(distance_km)) %>%
  select(-price_min_EUR,
         -duration_min,
         -distance_km,
         -frequency_tpw) %>%
  select(Outcome, everything())
test <- test %>%
  mutate(log_price = log(price_min_EUR),
         log_duration = log(duration_min),
         log_dist = log(distance_km)) %>%
  select(-price_min_EUR,
         -duration_min,
         -distance_km,
         -frequency_tpw) %>%
  select(Outcome, everything())
scale <- preProcess(train[,c(6:8)], method = c("center", "scale"))
train[,c(6:8)] <- predict(scale, newdata = train[,c(6:8)])
test[,c(6:8)] <- predict(scale, newdata = test[,c(6:8)])
# Modeling
set.seed(111)
model_LDA <- MASS::lda(Outcome ~ .,
                       data = train,
                       method = "mve")
pr <- predict(model_LDA, test, type = "prob")
cl <- ifelse(pr$posterior[,2] >= 0.5191759, 1, 0)
confusionMatrix(factor(cl), test$Outcome, positive = "1")$byClass

#===============================================================================
# PREDICTING
#===============================================================================
new_dataset <- read_excel("/Users/miss_viktoriia/Documents/CheapTrip/bus_without_labels.xlsx") %>%
  select(from_id,
         to_id,
         price_min_EUR,
         duration_min,
         distance_km,
         transport_id) %>%
  filter(transport_id == 2) %>%
  select(-transport_id) %>%
  filter((from_id %in% c(100:386)) & (to_id %in% c(100:386)))

from <- left_join(new_dataset, locations_from, by = c("from_id" = "from_id"))
to <- left_join(from, locations_to, by = c("to_id" = "to_id"))
data_prediction <- to %>%
  select(price_min_EUR,
         duration_min,
         distance_km,
         from_latitude,
         from_longitude,
         to_latitude,
         to_longitude)
lat <- preProcess(data_prediction[,c(4,6)], method = "range",
                             rangeBounds = c(0.49, 1.01))
data_prediction[,c(4,6)] <- predict(lat, newdata = data_prediction[,c(4,6)])
long <- preProcess(data_prediction[,c(5,7)], method = "range",
                              rangeBounds = c(-0.15, 0.66))
data_prediction[,c(5,7)] <- predict(long, newdata = data_prediction[,c(5,7)])
data_prediction <- data_prediction %>%
  mutate(log_price = log(price_min_EUR),
         log_duration = log(duration_min),
         log_dist = log(distance_km)) %>%
  select(-price_min_EUR,
         -duration_min,
         -distance_km)
data_prediction[,c(5:7)] <- predict(scale, newdata = data_prediction[,c(5:7)])
bus_predict <- predict(model_LDA, data_prediction, type = "prob")
class <- ifelse(bus_predict$posterior[,2] >= 0.5191759, 1, 0)

data_prediction <- new_dataset %>%
  mutate(Predicted_Outcome = class)
buses_valid_trips <- data_prediction %>%
  filter(Predicted_Outcome == 0)
buses_invalid_trips <- data_prediction %>%
  filter(Predicted_Outcome == 1)

write_xlsx(buses_valid_trips,"/Users/miss_viktoriia/Documents/CheapTrip/buses_valid_trips.xlsx")
write_xlsx(buses_invalid_trips,"/Users/miss_viktoriia/Documents/CheapTrip/buses_invalid_trips.xlsx")
