from database.model.resource import Resource


class Agent(Resource):
    """
    Many resources, such as organisation and member, are a type of Agent
    and should therefore inherit from this Agent class.
    Shared fields can be defined on this class.

    Notice the difference between Agent and AgentTable.
    The latter enables defining a relationship to "any Agent",
    by making sure that the identifiers of all resources that
    are Agents, are unique over the Agents.
    """
