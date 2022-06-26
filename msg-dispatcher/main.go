package main

import (
	"encoding/json"
	"fmt"
	"github.com/gofiber/fiber/v2"
	//"github.com/gofiber/template/pug"
	"io/ioutil"
	"log"
	"time"
	"strconv"
)

type ModelRecord struct {
	ID        string `json:"id"`
	Name      string `json:"name"`
	Descr     string `json:"description"`
	ModDate   string `json:"last-modified"`
	Validated string `json:"validated"`
	DocDate   string `json:"model-document-date"`
}

/* func bobo(){
 fmt.Println("Bobo!")
} */

var PORT int =5001  

type ModelRecords struct {
	Records []ModelRecord `json:"models"`
}

type ModelRecordsPtr struct {
	Records []*ModelRecord
}

func GetDBData(fileName string, modelData *ModelRecords) *ModelRecords {
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		panic(err)
	}
	if err := json.Unmarshal(data, &modelData); err != nil {
		panic(err)
	}

	return modelData
}

func GetDBDataPtrs(fileName string, modelData *ModelRecordsPtr) []*ModelRecord {

	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		panic(err)
	}

	if err := json.Unmarshal(data, &modelData); err != nil {
		panic(err)
	}
	return modelData.Records
}

func main() {

	var modelData ModelRecords // `json:""`
	//var modelDataPtr ModelRecordsPtr
	dbFileName := "../view-engine/data.json"
	app := fiber.New()

	//test := GetDBDataPtrs(dbFileName, &modelDataPtr)

	app.Use(func(c *fiber.Ctx) error {
		fmt.Println("-----------------------------------------------------")
		fmt.Println("GO Server for Msg Dispatcher called at: ", time.Now())
		fmt.Println("Method: ", c.Method(), "; Body: ", c.Body())
		fmt.Println("-----------------------------------------------------")
		return c.Next()
	})

	app.Get("/house", func(c *fiber.Ctx) error {
		return c.SendString("GO-LANG Msg Dispatcher is Running ...")
	})

	app.Get("/", func(c *fiber.Ctx) error {
		unMarshaledData := GetDBData(dbFileName, &modelData)
		currTime := time.Now()
		timeStr := currTime.String()
		fmt.Println("...", c.Method(), " at :", timeStr)
		fmt.Println(unMarshaledData.Records)
		c.JSON(unMarshaledData.Records)

		return nil
	})

	app.Put("/update/:ID/:ModDate/:Validated", func(c *fiber.Ctx) error {
		UPDATED_FLG := false
		unMarshaledData := GetDBData(dbFileName, &modelData)
		maxLen := len(unMarshaledData.Records)
		fmt.Println("ORIGINAL DB: ", unMarshaledData.Records)
		for k := 0; k < maxLen; k++ {

			model := &unMarshaledData.Records[k] //.Name = "Baba"
			if model.ID == c.Params("ID") {
				fmt.Println("Model ID match: ", model.ID)
				model.ModDate, model.Validated = c.Params("ModDate"), c.Params("Validated")
				fmt.Println("New ModDate: ", model.ModDate)
				UPDATED_FLG = true
				//model.Name = "Yesu Nye Afetor La"
			}
			//fmt.Println

		}

		if UPDATED_FLG {
			fmt.Println("UPDATED DB: ", unMarshaledData.Records)
		} else {
			fmt.Println("REQUEST", c.Request(), "RESULTED IN NO UPDATES")
		}
		marshaledData, err := json.Marshal(unMarshaledData)

		if err!=nil {
			panic(err)
		}
		err = ioutil.WriteFile(dbFileName, marshaledData, 0644)

		if err == nil {
			return nil
		} else {
			return err
		}

	})
	fmt.Println("Msg Dispatcher Server Started ...", time.Now(), "at localhost:", strconv.Itoa(PORT))
	log.Fatal(app.Listen(":" + strconv.Itoa(PORT)))
}
