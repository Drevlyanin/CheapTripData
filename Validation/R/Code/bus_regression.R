library(tidyverse)
library(caret)
library(readxl)
library(forcats)

#-------------------------------------------------------------------------------
bus_valid <- read_excel("/Users/miss_viktoriia/Documents/CheapTrip/buses_valid_trips.xlsx")
bus_invalid <- read_excel("/Users/miss_viktoriia/Documents/CheapTrip/buses_invalid_trips.xlsx")
bus <- rbind(bus_valid, bus_invalid)
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
bus <- connection_to %>%
  select(price_min_EUR,
         duration_min,
         distance_km,
         from_latitude,
         from_longitude,
         to_latitude,
         to_longitude,
         Predicted_Outcome)
bus_for_modeling <- bus
summary(bus_for_modeling)

bus_for_modeling <- bus_for_modeling %>%
  mutate(log_price = log(price_min_EUR),
         log_duration = log(duration_min),
         log_dist = log(distance_km)) %>%
  select(-price_min_EUR,
         -duration_min,
         -distance_km)
summary(bus_for_modeling)


lat <- preProcess(bus_for_modeling[,c(1,3)], method = "range",
                  rangeBounds = c(0.49, 1.01))
bus_for_modeling[,c(1,3)] <- predict(lat, newdata = bus_for_modeling[,c(1,3)])
long <- preProcess(bus_for_modeling[,c(2,4)], method = "range",
                   rangeBounds = c(-0.15, 0.66))
bus_for_modeling[,c(2,4)] <- predict(long, newdata = bus_for_modeling[,c(2,4)])

valid <- bus_for_modeling %>%
  filter(Predicted_Outcome == 0) %>%
  select(-Predicted_Outcome)
invalid <- bus_for_modeling %>%
  filter(Predicted_Outcome == 1) %>%
  select(-Predicted_Outcome)
#-------------------------------------------------------------------------------
#Split
set.seed(147)
i <- createDataPartition(valid$log_price, p = .8, list = FALSE)
train <- valid[ i,]
test  <- valid[-i,]
#Scale
scale_logs <- preProcess(train[, c(6,7)], method = c("center", "scale"))
train[,c(6,7)] <- predict(scale_logs, newdata = train[,c(6,7)])
test[,c(6,7)] <- predict(scale_logs, newdata = test[,c(6,7)])
invalid[,c(6,7)] <- predict(scale_logs, newdata = invalid[,c(6,7)])
#-------------------------------------------------------------------------------
#Modeling
model_kknn <- caret::train(log_price ~ ., 
                           data = train, 
                           method = "kknn",
                           tuneGrid = data.frame(kmax = 2,
                                                 distance = 4,
                                                 kernel = "triangular"),
                           metric = "MAE")
forecast::accuracy(as.vector(exp(predict(model_kknn, test))), exp(test$log_price))


pred_for_invalid <- exp(predict(model_kknn, invalid))

bus_invalid <- bus_invalid %>%
  mutate(Predicted_Price = pred_for_invalid) %>%
  select(-Predicted_Outcome)
writexl::write_xlsx(bus_invalid,"/Users/miss_viktoriia/Documents/CheapTrip/bus_invalid_with_prediction.xlsx")
