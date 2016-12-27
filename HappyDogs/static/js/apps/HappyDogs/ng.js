var angularApp = angular.module('HappyDogs' , ['ngResource']);

angularApp.controller('HappyDogsHomeCalendar' , [ '$scope' , '$resource' , HappyDogsHomeCalendar ]).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

angularApp.controller('HappyDogsAdminDog' , [ '$scope' , '$resource' , HappyDogsAdminDog ]).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

function HappyDogsAdminDog($scope, $resource , $http){
    $scope.LoginDisplay = false;
    $scope.detailDisplay = false;
    $scope.listDisplay = false;
    $scope.addDisplay = false;
    $scope.addVisitDisplay = false;
    $scope.addDogVisitUUID = null;
	$scope.HappyDogsHomeCalendarDetailResource = $resource(
		'/rest/happy_dogs/dogs.json' ,
		{
		} ,
		{
			get : {
				method : 'JSON'
			} ,
		}
	);
	$scope.HappyDogsDogDetailResource = $resource(
		'/rest/happy_dogs/dog.json' ,
		{
            uuid : '@uuid' ,
		} ,
		{
			get : {
				method : 'JSON'
			} ,
		}
	);
	$scope.HappyDogsDogUpdateDetailResource = $resource(
		'/rest/happy_dogs/update_dog.json' ,
		{
            uuid : '@uuid' ,
            first_name: '@first_name' ,
            last_name: '@last_name' ,
		} ,
		{
			get : {
				method : 'JSON'
			} ,
		}
	);
	$scope.HappyDogsDogAddDetailResource = $resource(
		'/rest/happy_dogs/add_dog.json' ,
		{
            first_name: '@first_name' ,
            last_name: '@last_name' ,
		} ,
		{
			get : {
				method : 'JSON'
			} ,
		}
	);
	$scope.HappyDogsDogAddVisitDetailResource = $resource(
		'/rest/happy_dogs/add_dog_visit.json' ,
		{
            start_date: '@start_date' ,
            end_date: '@end_date' ,
            uuid: '@uuid' ,
		} ,
		{
			get : {
				method : 'JSON'
			} ,
		}
	);
	$scope.HappyDogsHomeCalendarDetailResource.get().$promise.then(function(data){
		$scope.LoginDisplay = false;
		$scope.listDisplay = true;
		$scope.dogs = data.data.dogs;
	});

	$scope.viewDogDetail = function(uuid){
	    $scope.LoginDisplay = true;
	    $scope.listDisplay = false;
        $scope.HappyDogsDogDetailResource .get({
            uuid : uuid ,
        }).$promise.then(function(data){
            $scope.dogDetail = data.data.dog;
            $scope.detailDisplay = true;
            $scope.LoginDisplay = false;
        });
	}

	$scope.updateDogDetail = function(uuid){
	    $scope.LoginDisplay = true;
	    $scope.detailDisplay = false;
        $scope.HappyDogsDogUpdateDetailResource.get({
            uuid : uuid ,
            first_name : $scope.dogDetail.first_name ,
            last_name : $scope.dogDetail.last_name
        }).$promise.then(function(data){
            $scope.dogDetail = data.data.dog;
            $scope.detailDisplay = true;
            $scope.LoginDisplay = false;
            if($scope.dogDetail.saved == false){
                if($scope.dogDetail.error_message == ""){
                    alert('There has been an error, please try again later.')
                }else{
                    alert($scope.dogDetail.error_message)
                }

            }
        });
	}

	$scope.addDogVisit = function(uuid){
	    $scope.listDisplay = false;
	    $scope.addVisitDisplay = true;
	    $scope.addDogVisitUUID = uuid;
	}

	$scope.closeAddVisitDetail = function(){
	    $scope.listDisplay = true;
	    $scope.addVisitDisplay = false;
	}

	$scope.submitNewDogVisitDetail = function(){
        $scope.LoginDisplay = true;
        $scope.addVisitDisplay = false;
        $scope.HappyDogsDogAddVisitDetailResource.get({
            start_date : $scope.start_date ,
            end_date : $scope.end_date ,
            uuid : $scope.addDogVisitUUID
        }).$promise.then(function(data){
            $scope.addVisitDogDetail = data.data.dog;
            if($scope.addVisitDogDetail .added == false){
                if($scope.addVisitDogDetail .error_message == ""){
                    alert('There has been an error, please try again later.')
                }else{
                    alert($scope.addVisitDogDetail .error_message)
                }
            }
            $scope.HappyDogsHomeCalendarDetailResource.get().$promise.then(function(data){
                $scope.addVisitDisplay = false;
                $scope.listDisplay = true;
                $scope.LoginDisplay = false;
                $scope.dogs = data.data.dogs;
            });
        });
	}

	$scope.showAddDog = function(){
        $scope.listDisplay = false;
        $scope.addDisplay = true;
	}

	$scope.closeAddDetail = function(){
        $scope.HappyDogsHomeCalendarDetailResource.get().$promise.then(function(data){
            $scope.addDisplay = false;
            $scope.listDisplay = true;
            $scope.LoginDisplay = false;
            $scope.dogs = data.data.dogs;
        });
	}

	$scope.submitNewDogDetail = function(){
	    $scope.addDisplay = false;
	    $scope.LoginDisplay = true;
        $scope.HappyDogsDogAddDetailResource.get({
            first_name : $scope.addDogDetail.first_name ,
            last_name : $scope.addDogDetail.last_name
        }).$promise.then(function(data){
            $scope.addDogDetail = data.data.dog;
            if($scope.addDogDetail.added == false){
                if($scope.addDogDetail.error_message == ""){
                    alert('There has been an error, please try again later.')
                }else{
                    alert($scope.addDogDetail.error_message)
                }
            }
            $scope.HappyDogsHomeCalendarDetailResource.get().$promise.then(function(data){
                $scope.addDisplay = false;
                $scope.listDisplay = true;
                $scope.LoginDisplay = false;
                $scope.dogs = data.data.dogs;
            });
        });
	}

	$scope.closeViewDetail = function(){
        $scope.HappyDogsHomeCalendarDetailResource.get().$promise.then(function(data){
            $scope.detailDisplay = false;
            $scope.listDisplay = true;
            $scope.dogDetail = null;
            $scope.dogs = data.data.dogs;
        });
	}

}

function HappyDogsHomeCalendar($scope, $resource , $http){
    $scope.LoginDisplay = true;
    $scope.DetailDisplay = false;
    $scope.detail_date = '2016/12/12'
	$scope.HappyDogsHomeCalendarResource = $resource(
		'/rest/happy_dogs/home_calendar.json' ,
		{
            start_date : '@start_date' ,
            end_date : '@end_date' ,
		} ,
		{
			get : {
				method : 'JSON'
			} ,
		}
	);
	$scope.HappyDogsHomeCalendarDetailResource = $resource(
		'/rest/happy_dogs/detail_calendar.json' ,
		{
            date : '@start_date' ,
		} ,
		{
			get : {
				method : 'JSON'
			} ,
		}
	);
	$scope.HappyDogsHomeCalendarResource.get().$promise.then(function(data){
		$scope.LoginDisplay = false;
		$scope.weeks = data.data.weeks;
	});
	$scope.HappyDogsHomeCalendarFilterList = function(){
	    $scope.LoginDisplay = true;
        $scope.HappyDogsHomeCalendarResource.get({
            start_date : $scope.start_date ,
            end_date : $scope.end_date
        }).$promise.then(function(data){
            $scope.LoginDisplay = false;
            $scope.weeks = data.data.weeks;
        });
	};
	$scope.HappyDogsHomeCalendarShowDetail = function(date, week){
        $scope.LoginDisplay = true;
        $scope.DetailDisplay = false;
        $scope.HappyDogsHomeCalendarDetailResource.get({
            date : date
        }).$promise.then(function(data){
            $scope.DetailDisplay = true;
            $scope.LoginDisplay = false;
            $scope.day_detail = data.data.detail;
        });
	};
	$scope.HappyDogsHomeCalendarDetailClose = function(){
        $scope.DetailDisplay = false;
        $scope.LoginDisplay = false;
        $scope.day_detail = null;
	}
}