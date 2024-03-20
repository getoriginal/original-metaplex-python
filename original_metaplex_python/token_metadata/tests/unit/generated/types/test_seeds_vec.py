from dataclasses import asdict

from construct import Container

from original_metaplex_python.token_metadata.generated.types.seeds_vec import SeedsVec


def test_seeds_vec_to_encodable():
    seeds = [b"seed1", b"seed2"]
    seeds_vec = SeedsVec(seeds=seeds)
    encodable = seeds_vec.to_encodable()
    assert encodable == {"seeds": seeds}


def test_seeds_vec_from_decoded():
    seeds = [b"seed1", b"seed2"]
    decoded = Container(seeds=seeds)
    seeds_vec = SeedsVec.from_decoded(decoded)
    assert seeds_vec.seeds == seeds


def test_seeds_vec_to_json():
    seeds = [b"seed1", b"seed2"]
    seeds_vec = SeedsVec(seeds=seeds)
    json_obj = seeds_vec.to_json()
    assert json_obj == {"seeds": [list(b"seed1"), list(b"seed2")]}


def test_seeds_vec_from_json():
    seeds_json = {"seeds": [[115, 101, 101, 100, 49], [115, 101, 101, 100, 50]]}
    seeds_vec = SeedsVec.from_json(seeds_json)
    assert seeds_vec.seeds == [b"seed1", b"seed2"]


def test_seeds_vec_dataclass():
    seeds = [b"seed1", b"seed2"]
    seeds_vec = SeedsVec(seeds=seeds)
    assert asdict(seeds_vec) == {"seeds": seeds}
