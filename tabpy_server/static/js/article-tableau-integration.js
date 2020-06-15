(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();
    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        const queryString = window.location.search;
        console.log(queryString);
        $.get("https://datahub-api.intern-we.drift.azure.nrk.cloud/v1/service/sorted-list?id=nrkno&from=2020-05-12T22%3A00%3A00Z&to=2020-05-13T22%3A00%3A00Z&sort=asc&limit=1", function(resp) {
            var row = resp[0]
            console.log(row)
            var cols = []
            for ( const key in row )  {
                const obj = {}
                obj.id = key
                obj.alias = key
                if (row[key].getMonth) {
                    console.log("holanene")
                }
                switch (typeof (row[key])) {
                    case 'string':{
                        obj.dataType = tableau.dataTypeEnum.string
                        break
                    }
                    case 'number':{
                        obj.dataType = tableau.dataTypeEnum.float
                        break
                    }
                    default: {
                        obj.dataType = tableau.dataTypeEnum.string
                        break
                    }
                }
                if (key === 'from') {
                    obj.dataType = tableau.dataTypeEnum.date
                }
                if (key === 'to') {
                    obj.dataType = tableau.dataTypeEnum.date
                }
                if (key === 'published') {
                    obj.dataType = tableau.dataTypeEnum.date
                }
                cols.push(obj)
            }
            var tableInfo = {
                id: "articledata",
                alias: "articledataalias",
                columns: cols
            }
            schemaCallback([tableInfo]);
        })
    };
    // Download the data
    myConnector.getData = function(table, doneCallback) {
        const queryString = window.location.search;
        console.log(queryString);
        const urlParams = new URLSearchParams(queryString);
        const urlFrom = urlParams.get("from")
        var from = "2020-01-01T22%3A00%3A00Z"
        if (typeof urlFrom === "string") {
            from = urlFrom
        }
        const urlTo = urlParams.get("from")
        var to = "2020-06-08T22%3A00%3A00Z"
        if (typeof urlTo === "string") {
            from = urlTo
        }
        $.get("https://datahub-api.intern-we.drift.azure.nrk.cloud/v1/service/sorted-list?id=nrkno&from="+from+"&to="+to+"&sort=desc&limit=1000", function(resp) {
            table.appendRows(resp);
            doneCallback();
        });
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
        $("#submitButton").text("获取地震数据");
        clearInterval(pollLocale);
    }, 10);
};

getNEW = function () {
    return "Danielo"
}
