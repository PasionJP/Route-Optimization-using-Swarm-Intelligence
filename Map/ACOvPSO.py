#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .WazeRouteCalculator import *
from .PSOevaluate import *
from .ACOevaluate import *
from .MapShow import *
import logging
import os

class deliverCalc:
    def findCostPerDest(addresses, distance_or_time):    
        logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        logger.addHandler(handler)


        # from_address = '14.683037156885463, 121.02587075545517'
        # to_address = '14.708455871526157, 121.03840120358346'
        # addresses = ['14.683037156885463, 121.02587075545517', '14.708455871526157, 121.03840120358346']

        # addresses = ['14.683037156885463, 121.02587075545517', '14.734466039764392, 121.0578419643957', '14.686592853822372, 120.9770983695493', '14.591957923690291, 121.10419009699726']
        

        routes = []
        all_route_details = []

        for i in range(len(addresses)):
            for j in range(len(addresses)):
                if i != j:
                    from_address = addresses[i]
                    to_address = addresses[j]

                    route = WazeRouteCalculator(from_address, to_address)
                    try:
                        details = route.calc_route_info()
                        routes.append(details)
                        if distance_or_time == 0:
                            detail = [i, j, details[0][-2]]
                            all_route_details.append(detail)
                        else:
                            detail = [i, j, details[0][-1]]
                            all_route_details.append(detail)
                    except WRCError as err:
                        print(err)

        return all_route_details, routes

    # print(all_route_details)
    def calcPSO(all_route_details):
        psoVal, psoTime = ExecutePSO.runPSO(all_route_details)
        return psoVal, psoTime

    def calcACO(all_route_details):
        acoVal, acoTime = ExecuteACO.runACO(all_route_details)
        return acoVal, acoTime

class ACOvPSO:
    def generateCalculatedMap(addresses, distance_or_time, algo):
        # addresses = ['14.683037156885463, 121.02587075545517', '14.734466039764392, 121.0578419643957']
        # addresses = ['14.683037156885463, 121.02587075545517', '14.734466039764392, 121.0578419643957', '14.591957923690291, 121.10419009699726']

        costPerDeset, routes = deliverCalc.findCostPerDest(addresses, distance_or_time)
        # print(costPerDeset)
        if algo == 0:
            acoCalc, acoTime = deliverCalc.calcACO(costPerDeset)
            # print("ACO", acoCalc)
            # print("ROUTES", routes)
            
            # routes[1].insert(0, [float(routes[0][0]), float(routes[0][1])])
            # routes[1].append([float(routes[0][2]), float(routes[0][3])])
            # for i in range(len(routes)):
            address = []
            for i in range(len(acoCalc[0])):
                address.append(addresses[acoCalc[0][i]])

            add = []
            for j in range(len(address)):
                add.extend(address[j].split(', '))

            points = []
            for k in range(len(acoCalc[0])):
                r = [routes[i][0] for i in range(len(routes))]
                if k == len(acoCalc[0])-1:
                    l = 0
                else:
                    l = k+1
                ADD1 = [add[k*2], add[(k*2)+1], add[((l)*2)], add[((l)*2)+1]]
                ADD1_tuple = tuple(ADD1)
                positions = [index for index, entry in enumerate(r) if ADD1_tuple == tuple(entry[:4])]

                points.append(routes[positions[0]])

                # file = open("routes1.txt", "a")
                # a = file.write(str(points))
                # file.close()
            
            # dirname = os.path.dirname(__file__)
            dirname = os.path.dirname(os.path.abspath('__file__'))
            dir = r"template\ACOmap.html"
            save_location = os.path.join(dirname, dir)

            acoAddresses = mapShow(points, save_location)
            print("DONE!")
            return [acoCalc, acoAddresses], acoTime
        else:
            psoCalc, psoTime = deliverCalc.calcPSO(costPerDeset)
            # print("PSO", psoCalc)
            # print("ROUTES", routes)
            
            # routes[1].insert(0, [float(routes[0][0]), float(routes[0][1])])
            # routes[1].append([float(routes[0][2]), float(routes[0][3])])
            # for i in range(len(routes)):
            address = []
            for i in range(len(psoCalc[0])):
                address.append(addresses[psoCalc[0][i]])
            

            add = []
            for j in range(len(address)):
                add.extend(address[j].split(', '))

            points = []
            for k in range(len(psoCalc[0])):
                r = [routes[i][0] for i in range(len(routes))]
                if k == len(psoCalc[0])-1:
                    l = 0
                else:
                    l = k+1
                ADD1 = [add[k*2], add[(k*2)+1], add[((l)*2)], add[((l)*2)+1]]
                ADD1_tuple = tuple(ADD1)
                positions = [index for index, entry in enumerate(r) if ADD1_tuple == tuple(entry[:4])]

                points.append(routes[positions[0]])

                # file = open("routes1.txt", "a")
                # a = file.write(str(points))
                # file.close()

            dirname = os.path.dirname(os.path.abspath('__file__'))
            dir = r"template\PSOmap.html"
            save_location = os.path.join(dirname, dir)

            psoAddresses = mapShow(points, save_location)

            print("DONE!")
            return [psoCalc, psoAddresses], psoTime
            # return [acoCalc, psoCalc, acoAddresses, psoAddresses], acoTime, psoTime
            
# addresses = ['14.683037156885463, 121.02587075545517', '14.708455871526157, 121.03840120358346']
# x,y  = ACOvPSO.generateCalculatedMap(addresses, 0)
# print(y)