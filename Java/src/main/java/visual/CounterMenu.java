package visual;

import functional.Calculator;
import functional.classes.Location;
import functional.classes.Route;
import functional.classes.TransportationType;
import functional.classes.TravelData;
import maker.CSVMaker;
import maker.JSONMaker;
import maker.SQLMaker;
import maker.classes.TTMaker;
import parser.ParserForCounter;
import visual.classes.LoadType;
import visual.classes.LocationsFolderChecker;
import visual.classes.RoutesType;
import visual.classes.TravelDataFolderChecker;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;


public class CounterMenu {

    Font font = new Font("Arial",Font.PLAIN,14);
    LoadType loadTypes;
    RoutesType routesTypes;
    // common
    public JFrame CMFrame;
    JPanel CMPanel;

    // first part
    JPanel firstPanel;

    JPanel locationsPanel;
    JLabel locationsLabel;
    JTextField locationsPathField;

    JPanel travelDataPanel;
    JLabel travelDataLabel;
    JTextField travelDataPathField;

    // second part
    JPanel secondPanel;
    JLabel whatRoutes;
    JCheckBox routesCheck;
    JCheckBox fixedRoutesCheck;
    JCheckBox flyingRoutesCheck;

    // third part
    JLabel exportFeatures;
    JPanel thirdPanel;

    JPanel jsonPanel;
    JCheckBox jsonCheck;
    JTextField jsonPathField;
    JPanel csvPanel;
    JCheckBox csvCheck;
    JTextField csvPathField;
    JPanel sqlPanel;
    JCheckBox sqlCheck;
    JTextField sqlPathField;
    JPanel validationPanel;
    JCheckBox validationCheck;
    JTextField validationPathField;
    JPanel buttonPanel;
    JButton start;

    public CounterMenu() {
        loadTypes = new LoadType(false,false,false,false);
        routesTypes = new RoutesType(false,false,false);

        CMFrame = new JFrame("Main menu");
        CMPanel = new JPanel();
        Dimension partialDimension = new Dimension(400, 100);
        Dimension buttonDimension = new Dimension(150,50);
        Dimension panelsDimension = new Dimension(400,100);

        // first panel initializing
        firstPanel = new JPanel();

        locationsPanel = new JPanel();
        locationsLabel = new JLabel("CSV file with locations");
        locationsLabel.setFont(font);
        locationsPathField = new JTextField();
        locationsPanel.add(locationsLabel);
        locationsPanel.add(locationsPathField);
        locationsPanel.setLayout(new GridLayout(1,2,0,10));

        travelDataPanel = new JPanel();
        travelDataLabel = new JLabel("CSV file with travel_data");
        travelDataLabel.setFont(font);
        travelDataPathField = new JTextField();
        travelDataPanel.add(travelDataLabel);
        travelDataPanel.add(travelDataPathField);
        travelDataPanel.setLayout(new GridLayout(1,2,0,10));

        firstPanel.add(locationsPanel);
        firstPanel.add(travelDataPanel);
        firstPanel.setMaximumSize(partialDimension);
        firstPanel.setLayout(new GridLayout(2,1,0,20));

        whatRoutes = new JLabel("Choose routes to count",SwingConstants.CENTER);
        whatRoutes.setFont(font);

        // second panel initializing
        secondPanel = new JPanel();
        routesCheck = new JCheckBox("Routes");
        routesCheck.setFont(font);
        fixedRoutesCheck = new JCheckBox("Fixed routes");
        fixedRoutesCheck.setFont(font);
        flyingRoutesCheck = new JCheckBox("Flying routes");
        flyingRoutesCheck.setFont(font);
        secondPanel.add(whatRoutes);
        secondPanel.add(routesCheck);
        secondPanel.add(fixedRoutesCheck);
        secondPanel.add(flyingRoutesCheck);
        secondPanel.setPreferredSize(panelsDimension);
        secondPanel.setLayout(new GridLayout(4,1,0,7));

        // third panel initializing
        thirdPanel = new JPanel();
        exportFeatures = new JLabel("Choose export formats and folders");
        exportFeatures.setHorizontalAlignment(SwingConstants.CENTER);
        exportFeatures.setFont(font);

        jsonPanel = new JPanel();
        jsonCheck = new JCheckBox("JSON");
        jsonCheck.setFont(font);
        jsonPathField = new JTextField();
        jsonPanel.add(jsonCheck);
        jsonPanel.add(jsonPathField);
        jsonPanel.setLayout(new GridLayout(1,2,0,15));

        csvPanel = new JPanel();
        csvCheck = new JCheckBox("CSV");
        csvCheck.setFont(font);
        csvPathField = new JTextField();
        csvPanel.add(csvCheck);
        csvPanel.add(csvPathField);
        csvPanel.setLayout(new GridLayout(1,2,0,15));

        sqlPanel = new JPanel();
        sqlCheck = new JCheckBox("SQL");
        sqlCheck.setFont(font);
        sqlPathField = new JTextField();
        sqlPanel.add(sqlCheck);
        sqlPanel.add(sqlPathField);
        sqlPanel.setLayout(new GridLayout(1,2,0,15));

        validationPanel = new JPanel();
        validationCheck = new JCheckBox("Validation (csv)");
        validationCheck.setFont(font);
        validationPathField = new JTextField();
        validationPanel.add(validationCheck);
        validationPanel.add(validationPathField);
        validationPanel.setLayout(new GridLayout(1,2,0,15));

        thirdPanel.add(exportFeatures);
        thirdPanel.add(jsonPanel);
        thirdPanel.add(csvPanel);
        thirdPanel.add(sqlPanel);
        thirdPanel.add(validationPanel);
        thirdPanel.setPreferredSize(new Dimension(400,300));
        thirdPanel.setLayout(new GridLayout(5, 2,0,10));

        buttonPanel = new JPanel();
        buttonPanel.setPreferredSize(buttonDimension);
        start = new JButton("Start");
        start.setFont(font);
        start.setPreferredSize(buttonDimension);
        buttonPanel.add(start);
        start.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                ArrayList<TransportationType> types = TTMaker.typesInitializer();
                String locationsPath = locationsPathField.getText();
                String travelDataPath = travelDataPathField.getText();
                String csvFolderPath = csvPathField.getText();
                String jsonFolderPath = jsonPathField.getText();
                String sqlFolderPath = sqlPathField.getText();
                String validationFolderPath = validationPathField.getText();
                if (LocationsFolderChecker.locationsChecker(locationsPath)) {
                    if (TravelDataFolderChecker.travelDataChecker(travelDataPath)) {
                        if (routesCheck.isSelected()) {
                            routesTypes.setRoutesDefault(true);
                        }
                        if (fixedRoutesCheck.isSelected()) {
                            routesTypes.setFixedRoutesDefault(true);
                        }
                        if (flyingRoutesCheck.isSelected()) {
                            routesTypes.setFlyingRoutesDefault(true);
                        }
                        if (jsonCheck.isSelected()) {
                            loadTypes.setJsonLoad(true);
                        }
                        if (csvCheck.isSelected()) {
                            loadTypes.setCsvLoad(true);
                        }
                        if (sqlCheck.isSelected()) {
                            loadTypes.setSqlLoad(true);
                        }
                        if (validationCheck.isSelected()) {
                            loadTypes.setValidationLoad(true);
                        }
                        ArrayList<Location> locations = new ArrayList<>();
                        try {
                            locations = ParserForCounter.insertLocations(
                                    ParserForCounter.CSVoString(locationsPath));
                        } catch (IOException exc1) {
                            System.out.println("Problem with location insert");
                        }
                        ArrayList<TravelData> travelData = new ArrayList<>();
                        try {
                            travelData = ParserForCounter.insertTravelData(
                                    ParserForCounter.CSVoString(travelDataPath));
                        } catch (IOException exc2) {
                            System.out.println("Problem with travel_data insert");
                        }
                        if (routesTypes.isRoutesDefault()) {
                            ArrayList<TravelData> dataAll = Calculator.getDataWithoutRideShare(travelData);
                            ArrayList<Route> routes = Calculator.calculateRoutes(locations,dataAll,
                                    loadTypes.isValidationLoad(),validationFolderPath,"routes");
                            if (loadTypes.isCsvLoad() && !csvFolderPath.equals("")) {
                                CSVMaker.routesToFile(CSVMaker.routesToCSV(routes), csvFolderPath, "routes");
                            }
                            if (loadTypes.isJsonLoad() && !jsonFolderPath.equals("")) {
                                JSONMaker.jsonToFile(JSONMaker.routesJson(routes),jsonFolderPath,"routes");
                            }
                            if (loadTypes.isSqlLoad() && !jsonFolderPath.equals("")) {
                                SQLMaker.routesSQL(SQLMaker.routesToString(routes,"routes"),"routes",sqlFolderPath);
                            }
                        }
                        if (routesTypes.isFixedRoutesDefault()) {
                            ArrayList<TravelData> dataFixed = Calculator.getFixedDataWithoutRideShare(travelData);
                            ArrayList<Route> fixed_routes = Calculator.calculateRoutes(locations,dataFixed,
                                    loadTypes.isValidationLoad(),validationFolderPath,"fixed_routes");
                            if (loadTypes.isCsvLoad() && !csvFolderPath.equals("")) {
                                CSVMaker.routesToFile(CSVMaker.routesToCSV(fixed_routes), csvFolderPath, "fixed_routes");
                            }
                            if (loadTypes.isJsonLoad() && !jsonFolderPath.equals("")) {
                                JSONMaker.jsonToFile(JSONMaker.routesJson(fixed_routes),jsonFolderPath,"fixed_routes");
                            }
                            if (loadTypes.isSqlLoad() && !jsonFolderPath.equals("")) {
                                SQLMaker.routesSQL(SQLMaker.routesToString(fixed_routes,"fixed_routes"),"fixed_routes",sqlFolderPath);
                            }
                        }
                        if (routesTypes.isFlyingRoutesDefault()) {
                            ArrayList<TravelData> dataFlying = Calculator.getFlyingData(travelData);
                            ArrayList<Route> flying_routes = Calculator.calculateRoutes(locations,dataFlying,
                                    loadTypes.isValidationLoad(),validationFolderPath,"flying_routes");
                            if (loadTypes.isCsvLoad() && !csvFolderPath.equals("")) {
                                CSVMaker.routesToFile(CSVMaker.routesToCSV(flying_routes), csvFolderPath, "flying_routes");
                            }
                            if (loadTypes.isJsonLoad() && !jsonFolderPath.equals("")) {
                                JSONMaker.jsonToFile(JSONMaker.routesJson(flying_routes),jsonFolderPath,"flying_routes");
                            }
                            if (loadTypes.isSqlLoad() && !jsonFolderPath.equals("")) {
                                SQLMaker.routesSQL(SQLMaker.routesToString(flying_routes,"flying_routes"),"flying_routes",sqlFolderPath);
                            }
                        }

                        if (loadTypes.isCsvLoad() && !csvFolderPath.equals("")) {
                            CSVMaker.stringToFile(CSVMaker.locationsToCSV(locations),csvFolderPath,"locations");
                            CSVMaker.stringToFile(CSVMaker.transportationTypesToCSV(types),csvFolderPath,
                                    "transportation_types");
                            CSVMaker.stringToFile(CSVMaker.travelDataToCSV(travelData),csvFolderPath,"travel_data");
                        }
                        if (loadTypes.isJsonLoad() && !jsonFolderPath.equals("")) {
                            JSONMaker.jsonToFile(JSONMaker.locationsJson(locations),jsonFolderPath,"locations");
                            JSONMaker.jsonToFile(JSONMaker.transportationTypeJson(types),jsonFolderPath,
                                    "transportation_types");
                            JSONMaker.jsonToFile(JSONMaker.travelDataJson(travelData),jsonFolderPath,"travel_data");
                        }
                        if (loadTypes.isSqlLoad() && !sqlFolderPath.equals("")) {
                            SQLMaker.locationsSQL(SQLMaker.locationsToString(locations),sqlFolderPath);
                            SQLMaker.transportationTypesSQL(SQLMaker.transportationTypesToString(types),sqlFolderPath);
                            SQLMaker.travelDataSQL(SQLMaker.travelDataToString(travelData),sqlFolderPath);
                        }
                    }
                }
            }
        });

        CMPanel.add(firstPanel);
        CMPanel.add(secondPanel);
        CMPanel.add(thirdPanel);
        CMPanel.add(buttonPanel);

        CMPanel.setBorder(BorderFactory.createEmptyBorder(15,15,0,15));
        CMPanel.setLayout(new GridLayout(4, 1, 0, 20));

        CMFrame.add(CMPanel,BorderLayout.CENTER);
        CMFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        CMFrame.setBounds(200, 60, 40, 40);
        CMFrame.setPreferredSize(new Dimension(400,600));
        CMFrame.pack();
        CMFrame.setVisible(true);
    }
}