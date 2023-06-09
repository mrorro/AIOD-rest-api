from database.model.resource import Resource


class Agent(Resource):
    """
    Every organisation, member, and department has relationship to the Agent.
    Agent inherets from Resource.
    class Agent only defines an entity of type Agent, however the relationship
    between agent and an entity is defined in agent_table.py.
    """

    pass
