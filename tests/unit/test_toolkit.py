from typing import Tuple

import pytest
from bmt import Toolkit


@pytest.fixture(scope="module")
def toolkit():
    return Toolkit()


ASSOCIATION = "association"
BIOLOGICAL_ENTITY = "biological entity"
BIOLINK_BIOLOGICAL_ENTITY = "biolink:BiologicalEntity"
BIOLINK_SUBJECT = "biolink:subject"
BIOLINK_RELATED_TO = "biolink:related_to"
BIOLINK_NAMED_THING = "biolink:NamedThing"
NODE_PROPERTY = 'node property'
SYNONYM = "synonym"
ASSOCIATION_SLOT = "association slot"
HAS_POPULATION_CONTEXT = "population context qualifier"
CAUSES = "causes"
ENABLED_BY = "enabled by"
GENE = "gene"
GENE_OR_GENE_PRODUCT = "gene or gene product"
GENOMIC_ENTITY = "genomic entity"
INTERACTS_WITH = "interacts with"
MOLECULAR_ACTIVITY = "molecular activity"
NUCLEIC_ACID_ENTITY = "nucleic acid entity"
NAMED_THING = "named thing"
ORGANISM_TAXON = "organism taxon"
PHENOTYPIC_FEATURE = "phenotypic feature"
RELATED_TO = "related to"
SUBJECT = "subject"
THING_WITH_TAXON = "thing with taxon"
TREATMENT = "treatment"
ACTIVE_IN = "active in"
HAS_ACTIVE_COMPONENT = "has active component"

# aspect qualifier is abstract so not really a valid qualifier
ASPECT_QUALIFIER_NAME = "aspect qualifier"

ANATOMICAL_CONTEXT_QUALIFIER_NAME = "anatomical context qualifier"
ANATOMICAL_CONTEXT_QUALIFIER_CURIE = "biolink:anatomical_context_qualifier"
ANATOMICAL_CONTEXT_QUALIFIER_ENUM_NAME = "AnatomicalContextQualifierEnum"
ANATOMICAL_CONTEXT_QUALIFIER_ENUM_CURIE = "biolink:AnatomicalContextQualifierEnum"

SUBJECT_DIRECTION_QUALIFIER_NAME = "subject direction qualifier"
SUBJECT_DIRECTION_QUALIFIER_CURIE = "biolink:subject_direction_qualifier"
DIRECTION_QUALIFIER_ENUM_NAME = "DirectionQualifierEnum"
DIRECTION_QUALIFIER_ENUM_CURIE = "biolink:DirectionQualifierEnum"

SPECIES_CONTEXT_QUALIFIER_NAME= "species context qualifier"
SPECIES_CONTEXT_QUALIFIER_CURIE="biolink:species_context_qualifier"

# 'catalyst qualifier' has a mixin range 'macromolecular machine mixin'
CATALYST_QUALIFIER_NAME="catalyst qualifier"
CATALYST_QUALIFIER_CURIE="biolink:catalyst_qualifier"

# 'qualified predicate' is a qualifier use case in a class of its own
QUALIFIED_PREDICATE_NAME="qualified predicate"
QUALIFIED_PREDICATE_CURIE="biolink:qualified_predicate"

BIOLINK_ENTITY = 'biolink:Entity'


def test_get_model_version(toolkit):
    version = toolkit.get_model_version()
    assert version == "3.2.0"


def test_get_id_prefixes(toolkit):
    tclass = toolkit.get_element('biolink:Gene')
    print(tclass.id_prefixes)


def test_get_element_via_alias(toolkit):
    el = toolkit.get_element('definition')
    assert el.name == 'description'


def test_predicate_map(toolkit):
    mp = toolkit.get_predicate_mapping("augments")
    assert mp.get("biolink:object_aspect_qualifier") == 'activity or abundance'


def test_infores(toolkit):
    aragorn = toolkit.get_infores_details("infores:aragorn")
    assert aragorn["name"] == "ARAGORN"


def test_rna(toolkit):
    assert 'molecular entity' in toolkit.get_descendants(BIOLINK_ENTITY)
    assert 'microRNA' in toolkit.get_descendants(BIOLINK_ENTITY)
    assert 'biolink:MicroRNA' in toolkit.get_descendants(BIOLINK_ENTITY, formatted=True)


def test_get_element_by_mapping(toolkit):
    element_name = toolkit.get_element_by_mapping("RO:0003303")
    assert element_name == "causes"


def test_get_element_by_prefix(toolkit):
    elements = toolkit.get_element_by_prefix("UBERON:1234")
    assert "anatomical entity" in elements

    elements = toolkit.get_element_by_prefix("GO:1234")
    assert "molecular activity" in elements

    elements = toolkit.get_element_by_prefix("TEST:1234")
    assert "anatomical entity" not in elements


def test_get_all_elements(toolkit):
    elements = toolkit.get_all_elements()
    assert NAMED_THING in elements
    assert ASSOCIATION in elements
    assert RELATED_TO in elements
    assert "uriorcurie" in elements
    assert "thing does not exist" not in elements

    elements = toolkit.get_all_elements(formatted=True)
    assert "biolink:ThingDoesNotExist" not in elements
    assert BIOLINK_NAMED_THING in elements
    assert "biolink:GeneToGeneAssociation" in elements
    assert BIOLINK_RELATED_TO in elements
    assert "metatype:Uriorcurie" in elements
    assert "biolink:FrequencyValue" in elements


def test_get_all_entities(toolkit):
    entities = toolkit.get_all_entities()
    assert NAMED_THING in entities
    assert GENE in entities
    assert "disease" in entities
    assert ASSOCIATION not in entities
    assert RELATED_TO not in entities

    entities = toolkit.get_all_entities(formatted=True)
    assert BIOLINK_NAMED_THING in entities
    assert "biolink:Gene" in entities
    assert "biolink:Disease" in entities
    assert "biolink:Association" not in entities


def test_get_all_associations(toolkit):
    associations = toolkit.get_all_associations()
    assert ASSOCIATION in associations
    assert "gene to gene association" in associations
    assert NAMED_THING not in associations

    associations = toolkit.get_all_associations(formatted=True)
    assert "biolink:Association" in associations
    assert "biolink:GeneToGeneAssociation" in associations
    assert BIOLINK_NAMED_THING not in associations


def test_get_all_node_properties(toolkit):
    properties = toolkit.get_all_node_properties()
    assert "provided by" in properties
    assert "category" in properties
    assert "has gene" in properties
    assert RELATED_TO not in properties
    assert SUBJECT not in properties

    properties = toolkit.get_all_node_properties(formatted=True)
    assert "biolink:provided_by" in properties
    assert "biolink:category" in properties
    assert "biolink:has_gene" in properties
    assert BIOLINK_SUBJECT not in properties
    assert BIOLINK_RELATED_TO not in properties


def test_get_all_edge_properties(toolkit):
    properties = toolkit.get_all_edge_properties()
    assert SUBJECT in properties
    assert "object" in properties
    assert "frequency qualifier" in properties
    assert "not in the model" not in properties

    properties = toolkit.get_all_edge_properties(formatted=True)
    assert BIOLINK_SUBJECT in properties
    assert "biolink:object" in properties
    assert "biolink:frequency_qualifier" in properties


def test_get_element(toolkit):

    o = toolkit.get_element("drug intake")
    assert o and o.name == "drug exposure"

    o = toolkit.get_element("molecular function")
    assert o and o.name == MOLECULAR_ACTIVITY

    o = toolkit.get_element("molecular_function")
    assert o and o.name == MOLECULAR_ACTIVITY

    o = toolkit.get_element("cellular_component")
    assert o and o.name == "cellular component"

    o = toolkit.get_element("RNA Product")
    assert o and o.name == "RNA product"

    o = toolkit.get_element("rna product")
    assert o and o.name == "RNA product"


def test_is_node_property(toolkit):
    assert toolkit.is_node_property(NODE_PROPERTY)
    assert toolkit.is_node_property(SYNONYM)
    assert not toolkit.is_node_property(HAS_POPULATION_CONTEXT)
    assert not toolkit.is_node_property(CAUSES)
    assert not toolkit.is_node_property(GENE)


def test_is_association_slot(toolkit):
    assert toolkit.is_association_slot(ASSOCIATION_SLOT)
    assert toolkit.is_association_slot(HAS_POPULATION_CONTEXT)
    assert not toolkit.is_association_slot(SYNONYM)
    assert not toolkit.is_association_slot(CAUSES)
    assert not toolkit.is_association_slot(GENE)


def test_is_predicate(toolkit):
    assert toolkit.is_predicate(CAUSES)
    assert not toolkit.is_predicate(NAMED_THING)
    assert not toolkit.is_predicate(GENE)
    assert not toolkit.is_category(SYNONYM)
    assert not toolkit.is_category(HAS_POPULATION_CONTEXT)


def test_is_mixin(toolkit):
    assert not toolkit.is_mixin(NAMED_THING)
    assert toolkit.is_mixin("ontology class")
    assert not toolkit.is_mixin("this_does_not_exist")


def test_is_translator_canonical_predicate(toolkit):
    assert toolkit.is_translator_canonical_predicate("treats")
    assert not toolkit.is_translator_canonical_predicate("treated by")
    assert not toolkit.is_translator_canonical_predicate("this_does_not_exist")
    assert not toolkit.is_translator_canonical_predicate("completed by")
    assert toolkit.is_translator_canonical_predicate("regulates")


def test_has_inverse(toolkit):
    assert toolkit.has_inverse("completed by")
    assert not toolkit.has_inverse("this_does_not_exist")


def test_get_inverse(toolkit):
    assert toolkit.get_inverse(ACTIVE_IN) == HAS_ACTIVE_COMPONENT
    assert toolkit.get_inverse(HAS_ACTIVE_COMPONENT) == ACTIVE_IN
    sd = toolkit.get_element(ACTIVE_IN)
    assert toolkit.get_inverse(sd.name) == HAS_ACTIVE_COMPONENT


def test_category(toolkit):
    assert toolkit.is_category(NAMED_THING)
    assert toolkit.is_category(GENE)
    assert not toolkit.is_category(CAUSES)
    assert not toolkit.is_category("affects")
    assert not toolkit.is_category(GENE_OR_GENE_PRODUCT)


def test_is_qualifier(toolkit):
    assert toolkit.is_qualifier(SUBJECT_DIRECTION_QUALIFIER_NAME)
    assert toolkit.is_qualifier(SUBJECT_DIRECTION_QUALIFIER_CURIE)
    assert not toolkit.is_qualifier(DIRECTION_QUALIFIER_ENUM_NAME)
    assert not toolkit.is_qualifier(NAMED_THING)
    assert not toolkit.is_qualifier(CAUSES)
    assert not toolkit.is_qualifier("affects")
    assert not toolkit.is_qualifier(GENE_OR_GENE_PRODUCT)


def test_is_enum(toolkit):
    assert toolkit.is_enum(ANATOMICAL_CONTEXT_QUALIFIER_ENUM_NAME)
    assert toolkit.is_enum(ANATOMICAL_CONTEXT_QUALIFIER_ENUM_CURIE)
    assert toolkit.is_enum(DIRECTION_QUALIFIER_ENUM_NAME)
    assert not toolkit.is_enum(NAMED_THING)
    assert not toolkit.is_enum(CAUSES)
    assert not toolkit.is_enum("affects")
    assert not toolkit.is_enum(GENE_OR_GENE_PRODUCT)


def test_is_reachable_from_enum(toolkit):
    assert toolkit.is_reachable_from_enum(ANATOMICAL_CONTEXT_QUALIFIER_ENUM_NAME, "UBERON:0001981")  # Blood Vessel
    assert not toolkit.is_reachable_from_enum(ANATOMICAL_CONTEXT_QUALIFIER_ENUM_NAME, "pax:0001981")


@pytest.mark.parametrize(
    "query",
    [
        # method called with empty arguments fails gracefully
        ("", "", False), # Q0
        (SUBJECT_DIRECTION_QUALIFIER_NAME, "", False), # Q1
        ("", "upregulated", False), # Q2

        # 'aspect qualifier' is 'abstract', hence can't be instantiated (doesn't have a 'range')
        (ASPECT_QUALIFIER_NAME, "upregulated", False), # Q3

        # qualifier with value drawn from enum 'permissible values'
        (SUBJECT_DIRECTION_QUALIFIER_NAME, "upregulated", True), # Q4
        (SUBJECT_DIRECTION_QUALIFIER_CURIE, "upregulated", True), # Q5 - CURIE accepted here too

        # *** Use case currently not supported: RO term is exact_match to 'upregulated' enum
        # (SUBJECT_DIRECTION_QUALIFIER_NAME, "RO:0002213", True),  # Qx -

        # qualifier with value drawn from enum 'reachable from'
        (ANATOMICAL_CONTEXT_QUALIFIER_NAME, "UBERON:0001981", True), # Q6
        (ANATOMICAL_CONTEXT_QUALIFIER_CURIE, "UBERON:0001981", True), # Q7 - CURIE accepted here too

        # qualifier with value drawn from concrete Biolink category identifier spaces
        (SPECIES_CONTEXT_QUALIFIER_NAME, "NCBITaxon:9606", True), # Q8
        (SPECIES_CONTEXT_QUALIFIER_CURIE, "NCBITaxon:9606", True), # Q9 - CURIE accepted here too

        # qualifier with value drawn from concrete Biolink category identifier spaces
        (SPECIES_CONTEXT_QUALIFIER_NAME, "NCBITaxon:9606", True), # Q10
        (SPECIES_CONTEXT_QUALIFIER_CURIE, "NCBITaxon:9606", True), # Q11 - CURIE accepted here too

        # *** Another currently unsupported use case...
        # 'catalyst qualifier' has a mixin range 'macromolecular machine mixin'
        # 'GO:0032991' is exact match to 'macromolecular complex' which has
        #   'macromolecular machine mixin' as a mixin and also has id_prefixes including GO, so...
        # (CATALYST_QUALIFIER_NAME, "GO:0032991", True), # Qxx
        # (CATALYST_QUALIFIER_CURIE, "GO:0032991", True), # Qxx - CURIE accepted here too

        # mis-matched qualifier values or value types
        (SUBJECT_DIRECTION_QUALIFIER_NAME, "UBERON:0001981", False), # Q12
        (SPECIES_CONTEXT_QUALIFIER_NAME, "upregulated", False), # Q13
        (ANATOMICAL_CONTEXT_QUALIFIER_NAME, "upregulated", False), # Q14

        # *** Yetanuder currently unsupported use case...
        # 'qualified predicate' is a qualifier use case in a class of its own
        # Validation will require a priori knowledge of
        # the biolink:Association subclass e.g. biolink:ChemicalAffectsGeneAssociation,
        # that constrains the semantics of the edge in question
        # (QUALIFIED_PREDICATE_NAME, "causes", True),  # Qxx
        # (QUALIFIED_PREDICATE_CURIE, "causes", True),  # Qxx - CURIE accepted here too
    ]
)
def test_validate_qualifier(toolkit, query: Tuple[str, str, bool]):
    assert toolkit.validate_qualifier(query[0], query[1]) is query[2]


def test_is_permissible_value_of_enum(toolkit):
    assert toolkit.is_permissible_value_of_enum(ANATOMICAL_CONTEXT_QUALIFIER_ENUM_NAME, "UBERON:0001981")  # Blood Vessel
    assert toolkit.is_permissible_value_of_enum(DIRECTION_QUALIFIER_ENUM_NAME, "upregulated")
    assert toolkit.is_permissible_value_of_enum(DIRECTION_QUALIFIER_ENUM_CURIE, "upregulated")


def test_ancestors(toolkit):
    assert RELATED_TO in toolkit.get_ancestors(CAUSES)
    assert "biolink:ChemicalEntityOrGeneOrGeneProduct" in toolkit.get_ancestors(
        GENE, formatted=True
    )
    assert "biolink:GenomicEntity" in toolkit.get_ancestors(GENE, formatted=True)
    assert BIOLINK_RELATED_TO in toolkit.get_ancestors(CAUSES, formatted=True)
    assert "biolink:GeneOrGeneProduct" in toolkit.get_ancestors(GENE, formatted=True)
    assert "biolink:GeneOrGeneProduct" not in toolkit.get_ancestors(
        GENE, formatted=True, mixin=False
    )
    assert NAMED_THING in toolkit.get_ancestors(GENE)
    assert GENE_OR_GENE_PRODUCT in toolkit.get_ancestors(GENE)
    assert GENE_OR_GENE_PRODUCT not in toolkit.get_ancestors(GENE, mixin=False)
    assert BIOLINK_NAMED_THING in toolkit.get_ancestors(GENE, formatted=True)
    assert "biological entity" in toolkit.get_ancestors(GENE)
    assert "transcript" not in toolkit.get_ancestors(GENE)
    assert CAUSES in toolkit.get_ancestors(CAUSES)
    assert CAUSES in toolkit.get_ancestors(CAUSES, reflexive=True)
    assert CAUSES not in toolkit.get_ancestors(CAUSES, reflexive=False)
    assert "biolink:causes" in toolkit.get_ancestors(
        CAUSES, reflexive=True, formatted=True
    )
    assert GENOMIC_ENTITY in toolkit.get_ancestors(GENE)
    assert GENOMIC_ENTITY not in toolkit.get_ancestors(BIOLOGICAL_ENTITY)
    assert GENOMIC_ENTITY in toolkit.get_ancestors(GENOMIC_ENTITY, reflexive=True)
    assert GENOMIC_ENTITY not in toolkit.get_ancestors(GENOMIC_ENTITY, reflexive=False)
    assert THING_WITH_TAXON not in toolkit.get_ancestors(
        PHENOTYPIC_FEATURE, mixin=False
    )
    assert THING_WITH_TAXON in toolkit.get_ancestors(PHENOTYPIC_FEATURE)


def test_permissible_value_ancestors(toolkit):
    assert "increased" in toolkit.get_permissible_value_ancestors("upregulated", "DirectionQualifierEnum")
    assert "modified_form" in toolkit.get_permissible_value_ancestors("snp_form", "ChemicalOrGeneOrGeneProductFormOrVariantEnum")
    assert "increased" in toolkit.get_permissible_value_parent("upregulated", "DirectionQualifierEnum")


def test_ancestors_for_kgx(toolkit):
    ancestors1 = toolkit.get_ancestors(PHENOTYPIC_FEATURE, formatted=True, mixin=False)
    assert ancestors1 is not None
    assert len(ancestors1) == 5
    ancestors2 = toolkit.get_ancestors(PHENOTYPIC_FEATURE, formatted=True)
    assert ancestors2 is not None
    assert len(ancestors2) == 6


def test_descendants(toolkit):
    assert GENE in toolkit.get_descendants(GENE_OR_GENE_PRODUCT)
    assert GENE not in toolkit.get_descendants(GENE_OR_GENE_PRODUCT, mixin=False)
    assert MOLECULAR_ACTIVITY in toolkit.get_descendants("occurrent")
    assert GENE not in toolkit.get_descendants("outcome")
    assert GENE in toolkit.get_descendants(NAMED_THING)
    assert CAUSES in toolkit.get_descendants(RELATED_TO)
    assert INTERACTS_WITH in toolkit.get_descendants(RELATED_TO)
    assert PHENOTYPIC_FEATURE in toolkit.get_descendants(NAMED_THING)
    assert RELATED_TO not in toolkit.get_descendants(NAMED_THING)
    with pytest.raises(ValueError):
        toolkit.get_descendants('biolink:invalid')
    assert "biolink:PhenotypicFeature" in toolkit.get_descendants(
        NAMED_THING, formatted=True
    )
    assert "molecular activity_has output" not in toolkit.get_descendants(
        MOLECULAR_ACTIVITY, reflexive=True
    )
    assert "molecular activity_has output" not in toolkit.get_descendants(
        "has output", reflexive=True
    )
    assert "expressed in" in toolkit.get_descendants("located in")
    assert GENE in toolkit.get_descendants(GENE, reflexive=True)


def test_children(toolkit):
    assert CAUSES in toolkit.get_children("contributes to")
    assert "physically interacts with" in toolkit.get_children(INTERACTS_WITH)
    assert "transcript" in toolkit.get_children(NUCLEIC_ACID_ENTITY)
    assert GENE in toolkit.get_children(GENE_OR_GENE_PRODUCT)
    assert GENE not in toolkit.get_children(GENE_OR_GENE_PRODUCT, mixin=False)
    assert "biolink:Transcript" in toolkit.get_children(
        NUCLEIC_ACID_ENTITY, formatted=True
    )


def test_parent(toolkit):
    assert "contributes to" in toolkit.get_parent(CAUSES)
    assert INTERACTS_WITH in toolkit.get_parent("physically interacts with")
    assert BIOLOGICAL_ENTITY in toolkit.get_parent(GENE)
    assert BIOLINK_BIOLOGICAL_ENTITY in toolkit.get_parent(GENE, formatted=True)


def test_mapping(toolkit):
    assert len(toolkit.get_all_elements_by_mapping("SO:0000704")) == 1
    assert GENE in toolkit.get_all_elements_by_mapping("SO:0000704")

    assert len(toolkit.get_all_elements_by_mapping("MONDO:0000001")) == 1
    assert "disease" in toolkit.get_all_elements_by_mapping("MONDO:0000001")

    assert len(toolkit.get_all_elements_by_mapping("UPHENO:0000001")) == 1
    assert "affects" in toolkit.get_all_elements_by_mapping("UPHENO:0000001")


def test_get_slot_domain(toolkit):
    assert NAMED_THING in toolkit.get_slot_domain("ameliorates")
    assert "biological process or activity" in toolkit.get_slot_domain(ENABLED_BY)
    assert BIOLOGICAL_ENTITY in toolkit.get_slot_domain(
        ENABLED_BY, include_ancestors=True
    )
    assert BIOLINK_BIOLOGICAL_ENTITY in toolkit.get_slot_domain(
        ENABLED_BY, include_ancestors=True, formatted=True
    )
    # assert "entity" in toolkit.get_slot_domain("name")
    assert "entity" in toolkit.get_slot_domain("category")
    assert ASSOCIATION in toolkit.get_slot_domain("predicate")


def test_get_slot_range(toolkit):
    assert "disease or phenotypic feature" in toolkit.get_slot_range("treats")
    assert BIOLOGICAL_ENTITY in toolkit.get_slot_range("treats", include_ancestors=True)
    assert BIOLINK_BIOLOGICAL_ENTITY in toolkit.get_slot_range(
        "treats", include_ancestors=True, formatted=True
    )
    assert "label type" in toolkit.get_slot_range("name")


def test_get_all_slots_with_class_domain(toolkit):
    assert "has attribute" in toolkit.get_all_slots_with_class_domain(
        "entity", check_ancestors=True, mixin=True
    )
    assert "name" not in toolkit.get_all_slots_with_class_domain(
        TREATMENT, check_ancestors=False, mixin=False
    )
    assert "type" in toolkit.get_all_slots_with_class_domain(BIOLINK_ENTITY, check_ancestors=True, mixin=True)
    # we don't really have this use case in the model right now - where a domain's mixin has an attribute
    assert "has unit" in toolkit.get_all_slots_with_class_domain(
        "quantity value", check_ancestors=False, mixin=True
    )


def test_get_all_slots_with_class_range(toolkit):
    assert "in taxon" in toolkit.get_all_slots_with_class_range(ORGANISM_TAXON)
    assert "biolink:in_taxon" in toolkit.get_all_slots_with_class_range(
        ORGANISM_TAXON, formatted=True
    )
    assert SUBJECT in toolkit.get_all_slots_with_class_range(
        ORGANISM_TAXON, check_ancestors=True, mixin=False
    )
    assert "primary knowledge source" in toolkit.get_all_slots_with_class_range(
        "information resource", check_ancestors=True, mixin=False
    )
    assert "knowledge source" in toolkit.get_all_slots_with_class_range(
        "information resource", check_ancestors=True, mixin=True
    )


def test_get_all_predicates_with_class_domain(toolkit):
    assert "genetically interacts with" in toolkit.get_all_slots_with_class_domain(GENE)
    assert INTERACTS_WITH in toolkit.get_all_slots_with_class_domain(
        GENE, check_ancestors=True
    )
    assert "biolink:interacts_with" in toolkit.get_all_slots_with_class_domain(
        "gene", check_ancestors=True, formatted=True
    )
    assert "in complex with" in toolkit.get_all_slots_with_class_domain(
        GENE_OR_GENE_PRODUCT
    )
    assert "expressed in" in toolkit.get_all_slots_with_class_domain(
        GENE_OR_GENE_PRODUCT
    )
    assert RELATED_TO not in toolkit.get_all_slots_with_class_domain(
        GENE_OR_GENE_PRODUCT, check_ancestors=False, mixin=False
    )
    assert RELATED_TO not in toolkit.get_all_slots_with_class_domain(
        GENE_OR_GENE_PRODUCT, check_ancestors=True, mixin=True
    )


def test_get_all_predicates_with_class_range(toolkit):
    assert "manifestation of" in toolkit.get_all_predicates_with_class_range("disease")
    assert "target for" in toolkit.get_all_predicates_with_class_range(
        "disease", check_ancestors=True
    )
    assert (
        "biolink:target_for"
        in toolkit.get_all_predicates_with_class_range(
            "disease", check_ancestors=True, formatted=True
        )
    )
    assert RELATED_TO not in toolkit.get_all_predicates_with_class_range(
        "disease", check_ancestors=True, formatted=True
    )


def test_get_all_properties_with_class_domain(toolkit):
    assert "category" in toolkit.get_all_properties_with_class_domain("entity")
    assert "category" in toolkit.get_all_properties_with_class_domain(
        GENE, check_ancestors=True
    )
    assert "biolink:category" in toolkit.get_all_properties_with_class_domain(
        GENE, check_ancestors=True, formatted=True
    )

    assert "predicate" in toolkit.get_all_properties_with_class_domain(ASSOCIATION)
    assert "predicate" in toolkit.get_all_properties_with_class_domain(
        ASSOCIATION, check_ancestors=True
    )
    assert "biolink:predicate" in toolkit.get_all_properties_with_class_domain(
        ASSOCIATION, check_ancestors=True, formatted=True
    )


def test_get_all_properties_with_class_range(toolkit):
    assert "has gene" in toolkit.get_all_properties_with_class_range(GENE)
    assert SUBJECT in toolkit.get_all_properties_with_class_range(
        GENE, check_ancestors=True
    )
    assert "biolink:subject" in toolkit.get_all_properties_with_class_range(
        GENE, check_ancestors=True, formatted=True
    )


def test_get_value_type_for_slot(toolkit):
    assert "uriorcurie" in toolkit.get_value_type_for_slot(SUBJECT)
    assert "uriorcurie" in toolkit.get_value_type_for_slot("object")
    assert "string" in toolkit.get_value_type_for_slot("symbol")
    assert "biolink:CategoryType" in toolkit.get_value_type_for_slot(
        "category", formatted=True
    )


def test_get_all_types(toolkit):
    basic_descendants = {}

    # get_all_types()
    types = toolkit.get_all_types()

    for element in types:
        try:
            basic_descendants.update({
                element: toolkit.get_descendants(
                    element,
                    reflexive=False,
                    mixin=False,
                )
            })
        except Exception as e:
            assert False, f"Error getting descendants for {element}: {e}"


def test_get_all_multivalued_slots(toolkit):
    assert "synonym" in toolkit.get_all_multivalued_slots()
    assert "id" not in toolkit.get_all_multivalued_slots()
