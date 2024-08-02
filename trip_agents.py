from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from tools.calculator_tools import CalculatorTools
from typing import List
from langchain_core.callbacks import BaseCallbackHandler

# Initialize the language model
llm = ChatOpenAI(model='gpt-4o-mini')

class TripAgents:
    def __init__(self, callbacks: List[BaseCallbackHandler]):
        self.callbacks = callbacks

    def city_selection_agent(self):
        return Agent(
            role='City Selection Expert',
            goal='Select the best city based on weather, season, and prices',
            backstory='An expert in analyzing travel data to pick ideal destinations',
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
            ],
            verbose=True,
            llm=llm,
            callbacks=self.callbacks
        )

    def local_expert(self):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            backstory='A knowledgeable local guide with extensive information about the city, its attractions and customs',
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
            ],
            verbose=True,
            llm=llm,
            callbacks=self.callbacks
        )

    def travel_concierge(self):
        return Agent(
            role='Amazing Travel Concierge',
            goal='Create the most amazing travel itineraries with budget and packing suggestions for the city',
            backstory='Australian specialist in travel planning and logistics with decades of experience.',
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                CalculatorTools.calculate,
            ],
            verbose=True,
            llm=llm,
            callbacks=self.callbacks
        )
