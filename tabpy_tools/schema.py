import logging
import genson
import jsonschema


logger = logging.getLogger(__name__)


def _generate_schema_from_example_and_description(input, description):
    """
    With an example input, a schema is automatically generated that conforms
    to the example in json-schema.org. The description given by the users
    is then added to the schema.
    """
    s = genson.SchemaBuilder(None)
    s.add_object(input)
    input_schema = s.to_schema()

    if description is not None:
        if "properties" in input_schema:
            # Case for input = {'x':1}, input_description='not a dict'
            if not isinstance(description, dict):
                msg = f"{input} and {description} do not match"
                logger.error(msg)
                raise Exception(msg)

            for key in description:
                # Case for input = {'x':1},
                # input_description={'x':'x value', 'y':'y value'}
                if key not in input_schema["properties"]:
                    msg = f"{key} not found in {input}"
                    logger.error(msg)
                    raise Exception(msg)
                else:
                    input_schema["properties"][key]["description"] = description[key]
        else:
            if isinstance(description, dict):
                raise Exception(f"{input} and {description} do not match")
            else:
                input_schema["description"] = description

    try:
        # This should not fail unless there are bugs with either genson or
        # jsonschema.
        jsonschema.validate(input, input_schema)
    except Exception as e:
        logger.error(f"Internal error validating schema: {str(e)}")
        raise

    return input_schema


def generate_schema(input, output, input_description=None, output_description=None):
    """
    Generate schema from a given sample input and output.
    A generated schema can be passed to a server together with a function to
    annotate it with information about input and output parameters, and
    examples thereof. The schema needs to follow the conventions of JSON Schema
    (see json-schema.org).

    Parameters
    -----------
    input : any python type | dict
    output: any python type | dict
    input_description : str | dict, optional
    output_description : str | dict, optional

    References
    -----------
    - `Json Schema <http://json-schema.org/documentation.html>`

    Examples
    ----------
    .. sourcecode:: python
        For just one input parameter, state the example directly.
        >>> from tabpy_tools.schema import generate_schema
        >>> schema = generate_schema(
                              input=5,
                              output=25,
                              input_description='input value',
                              output_description='the squared value of input')
        >>> schema
        {'sample': 5,
         'input': {'type': 'integer', 'description': 'input value'},
         'output': {'type': 'integer', 'description': 'the squared value of input'}}
        For two or more input parameters, specify them using a dictionary.
        >>> import graphlab
        >>> schema = generate_schema(
                  input={'x': 3, 'y': 2},
                  output=6,
                  input_description={'x': 'value of x',
                                 'y': 'value of y'},
              output_description='x times y')
        >>> schema
        {'sample': {'y': 2, 'x': 3},
         'input': {'required': ['x', 'y'],
                   'type': 'object',
                   'properties': {'y': {'type': 'integer', 'description': 'value of y'},
                                  'x': {'type': 'integer', 'description': 'value of x'}}},
         'output': {'type': 'integer', 'description': 'x times y'}}
    """  # noqa: E501
    input_schema = _generate_schema_from_example_and_description(
        input, input_description
    )
    output_schema = _generate_schema_from_example_and_description(
        output, output_description
    )
    return {"input": input_schema, "sample": input, "output": output_schema}
