package functional;

import functional.classes.*;
import maker.CSVMaker;
import org.jgrapht.GraphPath;
import org.jgrapht.alg.shortestpath.DijkstraShortestPath;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.SimpleDirectedWeightedGraph;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Validator {

    public static String validate(HashMap<Integer, Integer> counter,
                                ArrayList<TravelData> directRoutes,
                                SimpleDirectedWeightedGraph<Integer, DefaultEdge> routeGraph
    ) {
        StringBuilder builder = new StringBuilder();
        List<TravelDataValidationStatus> validationList = new ArrayList<>();
        List<CounterFeature> list = new ArrayList<>();
        for (Map.Entry entry : counter.entrySet()) {
            CounterFeature feature = new CounterFeature();
            int id = (int) entry.getKey();
            int value = (int) entry.getValue();
            feature.setId(id);
            feature.setCount(value);
            list.add(feature);
        }

        List<CounterFeature> list_end = list.stream().sorted().filter(cf -> cf.getCount() > 70).collect(Collectors.toList());
        for (int i = 0; i < list_end.size(); i++) {
            CounterFeature feature = list_end.get(i);
            int feature_id = feature.getId();
            TravelData data_feature;
            float totalPrice = 0;
            for (int j = 0; j < directRoutes.size(); j++) {
                data_feature = directRoutes.get(j);
                int currentFromID = -1, currentToID = -1, bestTravelOptionID = -1;
                float minPrice = -1;
                if (data_feature.getId() == feature_id) {
                    StringBuilder travelData = new StringBuilder();
                    int from = data_feature.getFrom();
                    System.out.println("from = " + from);
                    int to = data_feature.getTo();
                    System.out.println("to = " + to);
                    routeGraph.removeEdge(routeGraph.removeEdge(from, to));
                    System.out.println("Удалено ребро от " + from + " и до " + to);
                    GraphPath<Integer, DefaultEdge> path = DijkstraShortestPath.findPathBetween(routeGraph,
                            from, to);
                    if (path == null) continue;
                    List<DefaultEdge> edgeList = path.getEdgeList();
                    if (edgeList == null || edgeList.size() == 0) {
                        continue;
                    }
                    for (int k = 0; k < edgeList.size(); k++) {
                        DefaultEdge edge = edgeList.get(k);
                        int edgeFrom = routeGraph.getEdgeSource(edge);
                        int edgeTo = routeGraph.getEdgeTarget(edge);
                        int id = 0;
                        int fromID = 0;
                        int toID = 0;
                        float euroPrice = 10000000;
                        for (int n = 0; n < directRoutes.size(); n++) {
                            TravelData data = directRoutes.get(n);
                            if (data.getFrom() == edgeFrom && data.getTo() == edgeTo) {
                                if (data.getEuro_price() < euroPrice) {
                                    id = data.getId();
                                    fromID = data.getFrom();
                                    toID = data.getTo();
                                    euroPrice = data.getEuro_price();
                                }
                            }
                        }
                        ArrayList<DirectRoute> routes = new ArrayList<>();
                        if (currentFromID == -1) {
                            currentFromID = fromID;
                            currentToID = toID;
                            minPrice = euroPrice;
                            bestTravelOptionID = id;
                            totalPrice = totalPrice + minPrice;
                            if (travelData.length() > 0) {
                                travelData.append(",");
                            }
                            travelData.append(bestTravelOptionID);
                            DirectRoute route = new DirectRoute(bestTravelOptionID,
                                    currentFromID,
                                    currentToID,
                                    minPrice);
                            routes.add(route);
                        } else if (currentFromID == fromID) {
                            if (minPrice > euroPrice) {
                                minPrice = euroPrice;
                                bestTravelOptionID = id;
                            }
                            totalPrice = totalPrice + minPrice;
                            if (travelData.length() > 0) {
                                travelData.append(",");
                            }
                            travelData.append(bestTravelOptionID);
                            DirectRoute route = new DirectRoute(bestTravelOptionID,
                                    currentFromID,
                                    currentToID,
                                    minPrice);
                            routes.add(route);
                        } else {
                            currentFromID = fromID;
                            currentToID = toID;
                            minPrice = euroPrice;
                            bestTravelOptionID = id;
                            totalPrice = totalPrice + minPrice;
                            if (travelData.length() > 0) {
                                travelData.append(",");
                            }
                            travelData.append(bestTravelOptionID);
                            DirectRoute route = new DirectRoute(bestTravelOptionID,
                                    currentFromID,
                                    currentToID,
                                    minPrice);
                            routes.add(route);
                        }
                    }
                    TravelDataValidationStatus status = new TravelDataValidationStatus();
                    status.setId(data_feature.getId());
                    status.setFrom(data_feature.getFrom());
                    status.setTo(data_feature.getTo());
                    status.setTransportation_type(data_feature.getTransportation_type());
                    status.setEuro_price(data_feature.getEuro_price());
                    status.setTime_in_minutes(data_feature.getTime_in_minutes());
                    status.setCounter(feature.getCount());
                    status.setAlternatePath(travelData.toString());
                    status.setAlternatePrice(totalPrice);
                    status.setStatus(data_feature.getEuro_price() / totalPrice);
                    validationList.add(status);

                    System.out.println("Маршрут идет по следующим direct routes " + travelData.toString());
                    System.out.println("Direct: id = " + data_feature.getId() + ", price = " + data_feature
                            .getEuro_price());
                    System.out.println("Alternative: " + travelData.toString() + ", price = " + totalPrice);
                    routeGraph.addEdge(from, to);
                    System.out.println("Добавлено ребро от " + from + " и до " + to);
                }
            }
        }

        for (int i = 0; i < validationList.size(); i++) {
            TravelDataValidationStatus status = validationList.get(i);
            builder.append("(")
                    .append(status.getId()).append(",")
                    .append(status.getFrom()).append(",")
                    .append(status.getTo()).append(",")
                    .append(status.getTransportation_type()).append(",")
                    .append(status.getEuro_price()).append(",")
                    .append(status.getTime_in_minutes()).append(",")
                    .append(status.getCounter()).append(",")
                    .append(status.getAlternatePath()).append(",")
                    .append(status.getAlternatePrice()).append(",")
                    .append(status.getStatus()).append(")");
            if (i == validationList.size() - 1) {
                builder.append(";");
            } else {
                builder.append(",");
            }
        }
        return builder.toString();
    }
}
