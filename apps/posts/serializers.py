from django.core.exceptions import FieldDoesNotExist

def serialize_instance_to_dict(instance, include_relations=None):
    """
    Serialize a single model instance to a dictionary representation.
    
    Args:
        instance: A Django model instance
        include_relations: Optional list of related field names to include
        
    Returns:
        dict: Serialized representation of the model
    """
    if include_relations is None:
        include_relations = []
    
    opts = instance._meta
    data = {}
    
    # Add regular fields
    for field in opts.concrete_fields:
        if not field.is_relation:
            data[field.name] = field.value_from_object(instance)
    
    # Process requested relations
    for relation_name in include_relations:
        # Handle dot notation for nested relations
        parts = relation_name.split('.', 1)
        field_name = parts[0]
        nested_relations = [parts[1]] if len(parts) > 1 else None
        
        # Try to get the related data
        try:
            # Check for forward relations (ForeignKey, OneToOneField)
            if hasattr(instance, field_name) and field_name in [f.name for f in opts.fields if f.is_relation]:
                related_instance = getattr(instance, field_name)
                if related_instance is None:
                    data[field_name] = None
                else:
                    data[field_name] = serialize_instance_to_dict(related_instance, include_relations=nested_relations)
            
            # Check for reverse relations (_set accessors or custom related_names)
            elif hasattr(instance, field_name):
                related_manager = getattr(instance, field_name)
                if hasattr(related_manager, 'all'):  # It's a RelatedManager
                    data[field_name] = serialize_queryset_to_list(related_manager.all(), include_relations=nested_relations)
                elif hasattr(related_manager, 'pk'):  # It's a single related object (OneToOneRel)
                    data[field_name] = serialize_instance_to_dict(related_manager, include_relations=nested_relations)
            
            # Check for many-to-many relations
            elif field_name in [f.name for f in opts.many_to_many]:
                data[field_name] = serialize_queryset_to_list(
                    getattr(instance, field_name).all(),
                    include_relations=nested_relations
                )
                
        except (AttributeError, FieldDoesNotExist):
            # Skip invalid field names
            continue
    
    return data


def serialize_queryset_to_list(queryset, include_relations=None):
    """
    Serialize a queryset of model instances to a list of dictionaries.
    
    Args:
        queryset: QuerySet or list of Django model instances
        include_relations: Optional list of related field names to include
        
    Returns:
        list: List of serialized model representations
    """
    return [
        serialize_instance_to_dict(instance, include_relations=include_relations) 
        for instance in queryset
    ]