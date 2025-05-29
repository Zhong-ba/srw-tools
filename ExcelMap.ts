import * as fs from 'fs';
import * as path from 'path';
import * as JSONbig from 'json-bigint';

const configPath = path.join(__dirname, 'scriptconfig.json');
const scriptConfig = JSONbig.parse(fs.readFileSync(configPath, 'utf8'));

const CONFIG = {
  EXCELS: scriptConfig.DataPath + "/ExcelOutput_Fix",
  TEXTMAP: scriptConfig.DataPath + "/TextMap",
  OUTPUT: scriptConfig.DataPath + "/MappedExcelOutput_EN",
  MAPPED: scriptConfig.DataPath + "/Mapped",
  LANGUAGES: ["TextMapEN"]
}

const EXCELS = new Map<string, any>();
const TEXTMAPS = new Map<string, any>();

const MAPPED_EXCELS: { [key: string]: { [key: string]: any } } = {
  ITEM: {}
}

async function main(): Promise<void> {
  const excels = fs.readdirSync(CONFIG.EXCELS);
  excels.forEach(fileName => {
    console.log(fileName);
    let data = fs.readFileSync(path.join(CONFIG.EXCELS, fileName), 'utf8');
    EXCELS.set(path.basename(fileName, ".json"), JSONbig.parse(data));
  });

  const textmaps = fs.readdirSync(CONFIG.TEXTMAP);
  textmaps.forEach(fileName => {
    let data = fs.readFileSync(path.join(CONFIG.TEXTMAP, fileName), 'utf8');
    TEXTMAPS.set(path.basename(fileName, ".json"), JSONbig.parse(data));
  });

  if (!fs.existsSync(CONFIG.OUTPUT)) {
    fs.mkdirSync(CONFIG.OUTPUT);
  }

  if (!fs.existsSync(CONFIG.MAPPED)) {
    fs.mkdirSync(CONFIG.MAPPED);
  }

  itemToId();

  EXCELS.forEach((excel, name) => {
    let output = mapObject(excel, name);
    fs.writeFileSync(path.join(CONFIG.OUTPUT, name + ".json"), JSONbig.stringify(output, null, 2));
    console.log(`Saved "${path.join(CONFIG.OUTPUT, name + ".json")}"`);
  });

  return;
}

function mapObject(item: any, excel: string) {
  if (Array.isArray(item)) return mapArray(item, excel);
  let result: { [key: string]: any } = {};
  Object.entries(item).map(([key, value]) => {
    if (key == "Hash") {
      getText(String(value), result);
    } else if (key == "ItemID") {
      result[key] = value;
      let item = MAPPED_EXCELS.ITEM[String(value)];
      if (item) result["ItemName"] = item;
    } else if (Array.isArray(value)) {
      result[key] = mapArray(value, excel);
    } else if (typeof value == "object") {
      result[key] = mapObject(value, excel);
    } else {
      result[key] = value;
    }
  });
  return result;
}

function mapArray(items: any[], excel: string): any[] {
  return items.map((item) => {
    if (Array.isArray(item)) return mapArray(item, excel);
    else if (typeof item == "object") return mapObject(item, excel);
    else return item;
  });
}

function getText(hash: string, result:{ [key: string]: any }): void {
  result["Hash"] = hash;
  CONFIG.LANGUAGES.forEach(lang => {
    let value = TEXTMAPS.get(lang)[hash];
    if (value) result[lang] = value;
  });
}

function itemToId() {
  if (!fs.existsSync(path.join(CONFIG.EXCELS, "ItemConfig.json"))) {
    console.error(`${path.join(CONFIG.EXCELS, "ItemConfig.json")} does not exist.`);
    return process.exit();
  }
  let data = JSONbig.parse(fs.readFileSync(path.join(CONFIG.EXCELS, "ItemConfig.json"), 'utf8'));
  Object.entries(data).map(([key, value]: [string, any]) => {
    let result: { [key: string]: any } = {};
    if (value.ItemName) {
      getText(value.ItemName.Hash, result)
    };
    MAPPED_EXCELS.ITEM[key] = result;
  });
  fs.writeFileSync(path.join(CONFIG.MAPPED, "ItemConfig.json"), JSONbig.stringify(MAPPED_EXCELS.ITEM, null, 2));
}

main();