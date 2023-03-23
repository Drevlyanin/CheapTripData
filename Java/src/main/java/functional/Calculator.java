package functional;

import functional.classes.*;
import maker.CSVMaker;
import maker.JSONMaker;
import maker.SQLMaker;
import org.jgrapht.GraphPath;
import org.jgrapht.alg.shortestpath.DijkstraShortestPath;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.SimpleDirectedWeightedGraph;
import parser.ParserForCounter;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Calculator {

    public static ArrayList<Route> calculateRoutes(ArrayList<Location> locations,
                                   ArrayList<TravelData> directRoutes,
                                   boolean validation,
                                   String folder,
                                   String routeType) {

        ArrayList<Route> routes_final = new ArrayList<>();
        int finalCount = 1;

        System.out.println("Started scanning routes");
        System.out.println("Getting locations");

        SimpleDirectedWeightedGraph<Integer, DefaultEdge> routeGraph =
                new SimpleDirectedWeightedGraph<>(DefaultEdge.class);
        for (int i = 0; i < locations.size(); i++) {
            routeGraph.addVertex(locations.get(i).getId());
        }

        for (int j = 0; j < directRoutes.size(); j++) {
            TravelData data = directRoutes.get(j);
            int Id = data.getId();
            int fromID = data.getFrom();
            int toID = data.getTo();
            float price = data.getEuro_price();
            DefaultEdge e = routeGraph.getEdge(fromID, toID);
            if (e != null) {
                System.out.println("Updating Price from: " + fromID + ", to: " + toID);
                if (routeGraph.getEdgeWeight(e) > price) routeGraph.setEdgeWeight(e, price);
            } else {
                if (fromID != toID) {
                    System.out.println("Adding to graph from: " + fromID + ", to: " + toID);
                    e = routeGraph.addEdge(fromID, toID);
                    routeGraph.setEdgeWeight(e, price);
                }
            }
        }
        HashMap<Integer, Integer> counter = new HashMap<>();
        for (Location from : locations) {
            System.out.println("Scanning from: " + from.getId());
            for (Location to : locations) {
                if (to.getId() == from.getId()) continue;
                System.out.println("--Scanning route from: " + from.getId() + " to: " + to.getId());
                GraphPath<Integer, DefaultEdge> path = DijkstraShortestPath.findPathBetween(routeGraph,
                        from.getId(), to.getId());
                if (path == null) continue;
                List<DefaultEdge> edgeList = path.getEdgeList();
                if (edgeList == null || edgeList.size() == 0) continue;
                StringBuilder travelData = new StringBuilder();
                float totalPrice = 0;
                int duration = 0;
                int currentFromID = -1, currentToID = -1, bestTravelOptionID = -1;
                float minPrice = -1;
                for (int i = 0; i < edgeList.size(); i++) {
                    DefaultEdge edge = edgeList.get(i);
                    int edgeFrom = routeGraph.getEdgeSource(edge);
                    int edgeTo = routeGraph.getEdgeTarget(edge);
                    int id = 0;
                    int fromID = 0;
                    int toID = 0;
                    float euroPrice = 10000000;
                    int minutes = 0;
                    for (int j = 0; j < directRoutes.size(); j++) {
                        TravelData data = directRoutes.get(j);
                        if (data.getFrom() == edgeFrom && data.getTo() == edgeTo) {
                            if (data.getEuro_price() < euroPrice) {
                                id = data.getId();
                                fromID = data.getFrom();
                                toID = data.getTo();
                                euroPrice = data.getEuro_price();
                                minutes = data.getTime_in_minutes();
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
                        counting(counter, bestTravelOptionID);
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
                        counting(counter, bestTravelOptionID);
                        DirectRoute route = new DirectRoute(bestTravelOptionID,
                                currentFromID,
                                currentToID,
                                minPrice);
                        routes.add(route);
                        System.out.println("Маршрут идет по следующим direct routes " + routes);
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
                        counting(counter, bestTravelOptionID);
                        DirectRoute route = new DirectRoute(bestTravelOptionID,
                                currentFromID,
                                currentToID,
                                minPrice);
                        routes.add(route);
                    }
                    duration = duration + minutes;
                }
                Route route1 = new Route(finalCount, from.getId(), to.getId(), totalPrice, duration,
                        travelData.toString());
                finalCount++;
                routes_final.add(route1);
            }
        }
        if (!folder.equals("") && validation) {
            CSVMaker.validationToFile(Validator.validate(counter,directRoutes,routeGraph),folder,routeType);
        }
        return routes_final;
    }

    public static ArrayList<TravelData> getFlyingData(ArrayList<TravelData> input) {
        ArrayList<TravelData> result = new ArrayList<>();
        for (int i = 0; i < input.size(); i++) {
            TravelData data = input.get(i);
            if (data.getTransportation_type() == 1) {
                result.add(data);
            }
        }
        return result;
    }

    public static ArrayList<TravelData> getFixedDataWithoutRideShare(ArrayList<TravelData> input) {
        ArrayList<TravelData> result = new ArrayList<>();
        for (int i = 0; i < input.size(); i++) {
            TravelData data = input.get(i);
            if ((data.getTransportation_type() != 1) && (data.getTransportation_type() != 8)) {
                result.add(data);
            }
        }
        return result;
    }

    public static ArrayList<TravelData> getDataWithoutRideShare(ArrayList<TravelData> input) {
        ArrayList<TravelData> result = new ArrayList<>();
        for (int i = 0; i < input.size(); i++) {
            TravelData data = input.get(i);
            if (data.getTransportation_type() != 8) {
                result.add(data);
            }
        }
        return result;
    }

    public static void counting(HashMap<Integer, Integer> counter, int travelData) {
        if (!counter.containsKey(travelData)) {
            counter.put(travelData, 1);
        } else {
            int count = counter.get(travelData);
            counter.put(travelData, count + 1);
        }
    }
}
