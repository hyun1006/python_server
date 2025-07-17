# print("나 실행되면 안됨")

# def add(a, b):
#     return a + b

# if __name__ == "__main__":
#     print("여기는 진짜 실행되면 안됨")


# 레이블 감지 코드
import boto3

def detect_labels_local_file(photo):

    client=boto3.client('rekognition')
   
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

    result =[]

    # Dog : 85.22%

    for label in response["Labels"]:
        name = label["Name"]
        confidence = label["Confidence"]
        
        result.append(f"{name} : {confidence:.2f}%")

    r = "<br/>".join(map(str, result))
    return r


def compare_faces(sourceFile, targetFile):
    client = boto3.client('rekognition')
    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')
    response = client.compare_faces(SimilarityThreshold=0,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        similarity = faceMatch['Similarity']

    imageSource.close()
    imageTarget.close()

    return f"동일 인물일 확률은 : {similarity:.2f}%입니다"