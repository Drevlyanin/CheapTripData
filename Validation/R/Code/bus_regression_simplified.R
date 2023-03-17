library(tidyverse)
library(caret)
library(readxl)


#-------------------------------------------------------------------------------
bus_valid <- read_excel("/Users/miss_viktoriia/Documents/CheapTrip/buses_valid_trips.xlsx") %>%
  select(-Predicted_Outcome)
bus_invalid <- read_excel("/Users/miss_viktoriia/Documents/CheapTrip/buses_invalid_trips.xlsx") %>%
  select(-Predicted_Outcome)
#Log transformation
valid <- bus_valid %>%
  mutate(log_price = log(price_min_EUR),
         log_duration = log(duration_min),
         log_dist = log(distance_km)) %>%
  select(-price_min_EUR,
         -duration_min,
         -distance_km,
         -from_id,
         -to_id)
invalid <- bus_invalid %>%
  mutate(log_price = log(price_min_EUR),
         log_duration = log(duration_min),
         log_dist = log(distance_km)) %>%
  select(-price_min_EUR,
         -duration_min,
         -distance_km,
         -from_id,
         -to_id)
#-------------------------------------------------------------------------------
#Split
set.seed(147)
i <- createDataPartition(valid$log_price, p = .8, list = FALSE)
train <- valid[ i,]
test  <- valid[-i,]
#Scale
scale_logs <- preProcess(train[, c(2,3)], method = c("center", "scale"))
train[,c(2,3)] <- predict(scale_logs, newdata = train[,c(2,3)])
test[,c(2,3)] <- predict(scale_logs, newdata = test[,c(2,3)])
invalid[,c(2,3)] <- predict(scale_logs, newdata = invalid[,c(2,3)])
#-------------------------------------------------------------------------------
#Modeling
model_kknn <- caret::train(log_price ~ ., 
                           data = train, 
                           method = "kknn",
                           tuneGrid = data.frame(kmax = 2,
                                                 distance = 20,
                                                 kernel = "triangular"))
forecast::accuracy(as.vector(exp(predict(model_kknn, test))), exp(test$log_price))


pred_for_invalid <- exp(predict(model_kknn, invalid))

bus_invalid <- bus_invalid %>%
  mutate(Predicted_Price = pred_for_invalid)
writexl::write_xlsx(bus_invalid,"/Users/miss_viktoriia/Documents/CheapTrip/bus_invalid_with_prediction.xlsx")
