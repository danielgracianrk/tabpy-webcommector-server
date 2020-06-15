(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();
    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "ATTR_CAMPAIGN",
            alias: "ATTR_CAMPAIGN",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "UNIT_GRP",
            alias: "UNIT_GRP",
            dataType: tableau.dataTypeEnum.float
        }, {
            id: "ID",
            alias: "ID",
            dataType: tableau.dataTypeEnum.string
        }
        ];

        var tableInfo = {
            id: "datafraLALALA",
            alias: "SISA",
            columns: cols
        };
        schemaCallback([tableInfo]);
    };
    // Download the data
    myConnector.getData = function(table, doneCallback) {
        var ATTR_CAMPAIGN = "",
            UNIT_GRP = 0

        $.get("http://localhost:8889/api.instarsuite.com/norwaytvov/IADS.asmx/GetData?iads_params=name:NRK-NO-API-1;password:wySGA3M9h;idLang:EN;idApp:3000;outformat:CSV;skipmetadata:1&tq=SELECT%20ATTR_CAMPAIGN,%20UNIT_GRP%20[ACC=1]%20FROM%20CALC_SPTS%20LIMIT%20%20OFFSET%200&tqx=reqId:1", function(resp) {
            const feat = resp.features,
                tableData = []
            a = resp.split('\n')

            for (var i = 1, len = a.length; i < len; i++) {
                const item = a[i].split(";")
                tableData.push({
                    "ATTR_CAMPAIGN": item[0],
                    "UNIT_GRP": item[1],
                    "ID": getNEW()
                })
            }
            table.appendRows(tableData);
            doneCallback();
        });
        console.log("no chuta")
    };

    tableau.registerConnector(myConnector);

    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        translateButton();
        $("#submitButton").click(function() {
            tableau.connectionName = "Get data"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();

// Values attached to the tableau object are loaded asyncronously.
// Here we poll the value of locale until it is properly loaded
// and defined, then we turn off the polling and translate the text.
var translateButton = function() {
    var pollLocale = setInterval(function() {
        if (tableau.locale) {
            switch (tableau.locale) {
                case tableau.localeEnum.china:
                    $("#submitButton").text("获取地震数据");
                    break;
                case tableau.localeEnum.germany:
                    $("#submitButton").text("Erhalten Erdbebendaten!");
                    break;
                case tableau.localeEnum.brazil:
                    $("#submitButton").text("Obter Dados de Terremoto!");
                    break;
                case tableau.localeEnum.france:
                    $("#submitButton").text("Obtenir les Données de Séismes!");
                    break;
                case tableau.localeEnum.japan:
                    $("#submitButton").text("地震データの取得");
                    break;
                case tableau.localeEnum.korea:
                    $("#submitButton").text("지진 데이터 가져 오기");
                    break;
                case tableau.localeEnum.spain:
                    $("#submitButton").text("Obtener Datos de Terremotos!");
                    break;
                default:
                    $("#submitButton").text("Get the data!");
            }
            clearInterval(pollLocale);
        }
    }, 10);
};

getNEW = function () {
    return "Danielo"
}
