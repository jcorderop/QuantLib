"""
Created: 22.05.2023
Description:
    * This Module defines the APIRouter for the yield curve End-Points.
"""
__author__ = "OE - JC"

import datetime

from app.util.config.ProjectSpecifics import *

__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from fastapi import Security, APIRouter
from datetime import date

from app.service.YieldCurve.PiecewiseYieldCurveService import PiecewiseYieldCurveService
from app.service.YieldCurve.ZeroCurveYieldCurveService import ZeroCurveYieldCurveService
from app.util.config.OpenApiDocumentation import Tags
from app.service.YieldCurve.BaseYieldCurveService import YieldCurveResponse
from app.service.YieldCurve.EnumYieldCurveService import PiecewiseMethod, YieldCurveFunctions, ZeroCurveMethod
from app.util.AzureCommonUtil import get_azure_scheme

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

END_POINT_YIELD_CURVE_VALUE_POINT_PIECE_WISE = "/marketdata/yieldcurve/piecewise/"
END_POINT_YIELD_CURVE_VALUE_POINT_ZERO_CURVE = "/marketdata/yieldcurve/zerocurve/"


@router.get(
    END_POINT_YIELD_CURVE_VALUE_POINT_PIECE_WISE + "{method}/{function}/{at_date}",
    dependencies=[Security(get_azure_scheme())],
    tags=[Tags.yield_curve],
    summary="Given yield curve type from Piece Wise Structure, function and date, it returns the point value on the curve.",
    response_description="Value Points",
)
async def fetch_yield_curve_points(method: PiecewiseMethod,
                                   function: YieldCurveFunctions,
                                   at_date: date) -> YieldCurveResponse:
    """
    This End-Point returns the point value on the curve for a given date.
    * Use **Method** based on: **PiecewiseMethod**
    * and a **Function** based on: **YieldCurveFunctions**
    """
    logger.info(f'Fetching yield curve point for Method: {method}, Function: {function}, At Date: {at_date}')
    service = PiecewiseYieldCurveService()
    response = await getattr(service, function.name)(method, at_date)
    logger.info('Benchmark Points Response: {}'.format(response))
    return response


@router.get(
    END_POINT_YIELD_CURVE_VALUE_POINT_ZERO_CURVE + "{method}/{function}/{at_date}",
    dependencies=[Security(get_azure_scheme())],
    tags=[Tags.yield_curve],
    summary="Given yield curve type from Zero Curve Structure, function and date, it returns the point value on the curve.",
    response_description="Value Points",
)
async def fetch_yield_curve_points(method: ZeroCurveMethod,
                                   function: YieldCurveFunctions,
                                   at_date: date) -> YieldCurveResponse:
    """
    This End-Point returns the point value on the curve for a given date.
    * Use **Method** based on: **ZeroCurveMethod**
    * and a **Function** based on: **YieldCurveFunctions**
    """
    logger.info(f'Fetching yield curve point for Method: {method}, Function: {function}, At Date: {at_date}')
    service = ZeroCurveYieldCurveService()
    response = await getattr(service, function.name)(method, at_date)
    logger.info('Benchmark Points Response: {}'.format(response))
    return response
