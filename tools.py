import json
import argparse

def populate_endpoints(pred_unit,port=5001):
    pred_unit.get("endpoint",{})["service_port"] = port
    pred_unit.get("endpoint",{})["service_host"] = "localhost"
    port += 1
    for child in pred_unit.get("children",[]):
        port = populate_endpoints(child,port=port)
    return port # returns next unallocated port

def extract_predictor(deployment,i=0):
    predictor = deployment.get("spec").get("predictors")[i]
    pred_unit = predictor.get("graph")
    populate_endpoints(pred_unit)
    return predictor

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    parser_gen_predictor = subparsers.add_parser("gen_predictor")
    parser_gen_predictor.add_argument("file",type=str,help="Path to the deployment json file")
    parser_gen_predictor.add_argument("--engine",type=str,default="./engine",help="Path to the engine folder")
    
    args = parser.parse_args()

    if args.command == "gen_predictor":
        deployment = json.load(open(args.file,'r'))
        predictor = extract_predictor(deployment)
        json.dump(predictor,open(args.engine+"/deploymentdef.json",'w'),indent=4)
        
    
